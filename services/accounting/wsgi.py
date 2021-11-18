from typing import Union

import jwt
from flask import Flask, request, render_template, url_for, redirect, Response

import db
import settings
from models import Role, User

app = Flask('accounting')


def authorize() -> Union[tuple[User, None], tuple[None, Response]]:
    token = request.cookies.get('AccessToken')
    if not token:
        response = redirect('http://localhost:4000/auth?redirect_url=http://localhost:4200/main')
        return None, response
    user_data = jwt.decode(token, settings.OAUTH_SECRET, algorithms=['HS256'])
    user = db.get_user_by_public_id(public_id=user_data['public_id'])
    return user, None


@app.route('/main')
def main_view():
    user, response = authorize()
    if response:
        return response
    if user.role in (Role.admin, Role.accountant):
        transactions = db.get_transactions()
        yearns = db.top_management_yearns()
        return render_template('accountant_view.html', transactions=transactions, yearns=yearns, user=user)
    transactions = db.get_transactions(user_id=user.public_id)
    balances = db.get_balances(user_id=user.public_id)
    return render_template('worker_view.html', transactions=transactions, balances=balances, user=user)


@app.route('/logout')
def logout():
    response = redirect(url_for('main_view'))
    response.delete_cookie('AccessToken')
    return response


if __name__ == '__main__':
    app.run()
