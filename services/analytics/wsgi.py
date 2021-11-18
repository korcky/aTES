import http
from typing import Union

import jwt
from flask import Flask, request, render_template, url_for, redirect, Response

import db
import settings
from models import Role, User

app = Flask('analytics')


def authorize() -> Union[tuple[User, None], tuple[None, Response]]:
    token = request.cookies.get('AccessToken')
    if not token:
        response = redirect('http://localhost:4000/auth?redirect_url=http://localhost:4300/main')
        return None, response
    user_data = jwt.decode(token, settings.OAUTH_SECRET, algorithms=['HS256'])
    user = db.get_user_by_public_id(public_id=user_data['public_id'])
    return user, None


@app.route('/main')
def main_view():
    user, response = authorize()
    if response:
        return response
    if user.role != Role.admin:
        return Response(f'No access for {user.role}', http.HTTPStatus.FORBIDDEN)
    management_yearns = db.get_management_yearns_for_today()
    below_zero_workers = db.get_below_zero_worker_count()
    most_expensive_tasks = db.get_most_expensive_tasks()
    return render_template(
        'main_view.html',
        user=user,
        management_yearns=management_yearns,
        below_zero_workers=below_zero_workers,
        most_expensive_tasks=most_expensive_tasks,
    )


@app.route('/logout')
def logout():
    response = redirect(url_for('main_view'))
    response.delete_cookie('AccessToken')
    return response


if __name__ == '__main__':
    app.run()
