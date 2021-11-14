import jwt
import http
from flask import Flask, request, render_template, url_for, redirect, Response

import db
import settings
from message_broker import cud_events, business_events
from models import Role

app = Flask('oauth')


@app.route('/auth')
def auth_screen():
    token = request.cookies.get('AccessToken')
    if not token:
        redirect_url = request.args.get('redirect_url', '/auth')
        return render_template('auth.html', redirect_url=redirect_url)
    data = jwt.decode(token, settings.OAUTH_SECRET, algorithms=['HS256'])
    return render_template('view.html', user=data)


@app.route('/login', methods=['POST'])
def login():
    email = request.form['email']
    pwd = request.form['pwd']
    redirect_url = request.args.get('redirect_url')
    response = redirect(redirect_url if redirect_url else url_for('auth_screen'))
    try:
        user = db.get_user(email=email, password=pwd)
    except Exception as e:
        return Response(f'Login error: {e}', status=http.HTTPStatus.BAD_REQUEST)
    access_token = jwt.encode(user.json_serializable(), settings.OAUTH_SECRET, algorithm='HS256')
    response.set_cookie('AccessToken', access_token)
    return response


@app.route('/register', methods=['POST'])
def register():
    email = request.form['email']
    pwd = request.form['pwd']
    redirect_url = request.args.get('redirect_url')
    response = redirect(redirect_url if redirect_url else url_for('auth_screen'))
    if db.is_user_exist(email=email):
        return render_template('auth.html', redirect_url=redirect_url)
    try:
        db.create_user(email=email, password=pwd)
        user = db.get_user(email=email, password=pwd)
    except Exception as e:
        return Response(f'Registration error: {e}', status=http.HTTPStatus.BAD_REQUEST)
    cud_events.user_created(user=user)
    access_token = jwt.encode(user.json_serializable(), settings.OAUTH_SECRET, algorithm='HS256')
    response.set_cookie('AccessToken', access_token)
    return response


@app.route('/update', methods=['POST'])
def update():
    token = request.cookies.get('AccessToken')
    if not token:
        redirect_url = request.args.get('redirect_url', '/auth')
        return render_template('auth.html', redirect_url=redirect_url)
    user = jwt.decode(token, settings.OAUTH_SECRET, algorithms=['HS256'])
    fields = {}
    for field in ['email', 'first_name', 'last_name']:
        if request.form.get(field):
            fields[field] = request.form[field]
    if fields:
        db.update_user(public_id=user['public_id'], **fields)
        cud_events.user_updated(fields)

    role = request.form.get('role')
    if role:
        role = Role(role)
        db.update_user(public_id=user['public_id'], role=role)
        business_events.role_updated(public_id=user['public_id'], new_role=role)
    return redirect(url_for('auth_screen'))


@app.route('/logout')
def logout():
    response = redirect(url_for('auth_screen'))
    response.delete_cookie('AccessToken')
    return response


if __name__ == '__main__':
    app.run()
