import jwt
import http
import random
from datetime import datetime
from flask import Flask, request, render_template, url_for, redirect, Response

import db
import settings
from message_broker import cud_events, business_events
from models import Role, Status

app = Flask('oauth')


def authorize():
    token = request.cookies.get('AccessToken')
    if not token:
        response = redirect('http://localhost:4000/auth?redirect_url=http://localhost:4100/main')
        return None, response
    user_data = jwt.decode(token, settings.OAUTH_SECRET, algorithms=['HS256'])
    user = db.get_user_by_public_id(public_id=user_data['public_id'])
    return user, None


@app.route('/main')
def main_view():
    user, response = authorize()
    if response:
        return response
    if user.role in (Role.admin, Role.manager):
        data = db.get_all_tasks()
        return render_template('manager_view.html', data=data, user=user)
    data = db.get_user_tasks(assignee_id=user.public_id)
    return render_template('worker_view.html', data=data, user=user)


@app.route('/create_task', methods=['POST'])
def create_task():
    user, response = authorize()
    if response:
        return response
    title = request.form['title']
    jira_id = request.form.get('jira_id')
    description = request.form['description']
    if '[' in title or ']' in title:
        return Response(f'Title must not contain "[" or "]"', http.HTTPStatus.BAD_REQUEST)
    try:
        workers_ids = db.get_all_workers_public_ids()
        assignee_id = random.Random(datetime.utcnow().timestamp()).choice(workers_ids)
        task = db.create_task(
            title=title,
            jira_id=jira_id,
            description=description,
            assignee_id=assignee_id,
        )
    except Exception as e:
        return Response(f'Create task error: {e}', http.HTTPStatus.BAD_REQUEST)
    cud_events.task_created(task=task)
    business_events.task_assigned(task=task)
    return redirect(url_for('main_view'))


@app.route('/close_task', methods=['POST'])
def close_task():
    user, response = authorize()
    if response:
        return response
    if user.role in (Role.admin, Role.manager):
        return Response(f'No access for {user.role}', http.HTTPStatus.FORBIDDEN)
    task_public_id = request.args.get('task_public_id')
    if not task_public_id:
        return Response('No task_public_id', http.HTTPStatus.BAD_REQUEST)
    task = db.get_task(public_id=task_public_id)
    if str(task.public_id) != str(user.public_id):
        return Response('You can\'t close this task', http.HTTPStatus.BAD_REQUEST)
    try:
        db.close_task(public_id=task_public_id)
    except Exception as e:
        return Response(f'Close task error: {e}', http.HTTPStatus.BAD_REQUEST)
    business_events.task_completed(task=task)
    return redirect(url_for('main_view'))


@app.route('/reassign_tasks', methods=['POST'])
def reassign_tasks():
    user, response = authorize()
    if response:
        return response
    if user.role not in (Role.admin, Role.manager):
        return Response(f'No access for {user.role}', http.HTTPStatus.FORBIDDEN)
    try:
        tasks = db.get_all_tasks(status=Status.open)
        workers_ids = db.get_all_workers_public_ids()
        shuffle = random.Random(datetime.utcnow().timestamp()).choices(workers_ids, k=len(tasks))
        for task, assignee_id in zip(tasks, shuffle):
            db.assign_to_task(public_id=task.public_id, assignee_id=assignee_id)
            business_events.task_assigned(task=task)
    except Exception as e:
        return Response(f'Reassign tasks error: {e}', http.HTTPStatus.BAD_REQUEST)
    return redirect(url_for('main_view'))


@app.route('/logout')
def logout():
    response = redirect(url_for('main_view'))
    response.delete_cookie('AccessToken')
    return response


if __name__ == '__main__':
    app.run()
