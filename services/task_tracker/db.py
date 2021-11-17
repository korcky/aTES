from contextlib import contextmanager
from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

import psycopg2

import settings
from models import Role, User, Task, Status


@contextmanager
def connection():
    _connection = psycopg2.connect(
        dbname=settings.DB_NAME,
        user=settings.DB_USER,
        password=settings.DB_PASS,
        host='task_tracker_postgres',
    )
    cursor = _connection.cursor()
    try:
        yield cursor
        _connection.commit()
    finally:
        cursor.close()
        _connection.close()


def create_user(
        public_id: str,
        email: str,
        first_name: Optional[str],
        last_name: Optional[str],
        role: Role,
        is_active: bool,
) -> None:
    with connection() as conn:
        conn.execute(
            'INSERT INTO users (public_id, email, first_name, last_name, role, is_active) '
            + f"VALUES ('{public_id}', '{email.lower()}', '{first_name}', '{last_name}', '{role.value}', '{is_active}');",
        )


def update_user(public_id: str, **fields: str):
    if not fields:
        return
    set_statements = [f"{k} = '{v}'" for k, v in fields.items()]
    with connection() as conn:
        conn.execute(
            f"UPDATE users SET {','.join(set_statements)} WHERE public_id = '{public_id}'"
        )


def get_user_by_public_id(
        public_id: str,
) -> User:
    with connection() as conn:
        conn.execute(
            'SELECT public_id, email, first_name, last_name, role, is_active '
            + f"FROM users WHERE public_id = '{public_id}';"
        )
        res = conn.fetchone()
        if not res:
            raise Exception('User not Found')
        return User(
            public_id=UUID(res[0]),
            email=res[1],
            first_name=res[2],
            last_name=res[3],
            role=Role(res[4]),
            is_active=res[5],
        )


def create_task(title, jira_id, description, assignee_id) -> Task:
    with connection() as conn:
        public_id = uuid4()
        conn.execute(
            'INSERT INTO tasks (public_id, assignee_id, title, jira_id, description, status) '
            + f"VALUES ('{uuid4()}', '{assignee_id}', {title}, {jira_id}, '{description}', '{Status.open.value}');",
        )
        return Task(
            public_id=public_id,
            assignee_id=assignee_id,
            title=title,
            jira_id=jira_id,
            description=description,
            status=Status.open,
            created_at=datetime.utcnow(),
        )


def get_task(public_id) -> Task:
    with connection() as conn:
        conn.execute(
            'SELECT public_id, assignee_id, title, jira_id, description, status, created_at '
            + f"FROM tasks WHERE public_id = '{public_id}'",
        )
        task = conn.fetchone()
        if not task:
            raise Exception('Task not Found')
        return Task(
            public_id=task[0],
            assignee_id=task[1],
            title=task[2],
            jira_id=task[3],
            description=task[4],
            status=Status(task[5]),
            created_at=task[6],
        )


def get_all_workers_public_ids() -> list[UUID]:
    with connection() as conn:
        conn.execute(f"SELECT public_id FROM users WHERE role = '{Role.worker.value}' AND is_active;")
        res = conn.fetchall()
        return [UUID(row[0]) for row in res]


def get_all_tasks(status: Optional[Status] = None) -> list[Task]:
    with connection() as conn:
        conn.execute(
            'SELECT public_id, assignee_id, title, jira_id, description, status, created_at '
            + 'FROM tasks ' + (f"WHERE status = '{status.value}' " if status else '')
            + 'ORDER BY created_at DESC',
        )
        res = conn.fetchall()
        return [
            Task(
                public_id=task[0],
                assignee_id=task[1],
                title=task[2],
                jira_id=task[3],
                description=task[4],
                status=Status(task[5]),
                created_at=task[6],
            )
            for task in res
        ]


def get_user_tasks(assignee_id: UUID) -> list[Task]:
    with connection() as conn:
        conn.execute(
            'SELECT public_id, assignee_id, title, jira_id, description, status, created_at '
            + 'FROM tasks '
            + f"WHERE assignee_id = '{assignee_id}' AND status = '{Status.open.value}' "
            + 'ORDER BY created_at DESC',
        )
        res = conn.fetchall()
        return [
            Task(
                public_id=task[0],
                assignee_id=task[1],
                title=task[2],
                jira_id=task[3],
                description=task[4],
                status=Status(task[5]),
                created_at=task[6],
            )
            for task in res
        ]


def close_task(public_id):
    with connection() as conn:
        conn.execute(
            'UPDATE tasks '
            + f"SET status = '{Status.closed.value}' "
            + f"WHERE public_id = '{public_id}';",
        )


def assign_to_task(public_id, assignee_id):
    with connection() as conn:
        conn.execute(
            'UPDATE tasks '
            + f"SET assignee_id = '{assignee_id}' "
            + f"WHERE public_id = '{public_id}';",
        )
