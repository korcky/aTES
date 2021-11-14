from contextlib import contextmanager
from typing import Optional
from uuid import uuid4

import psycopg2

import security
import settings
from models import Role, User


@contextmanager
def connection():
    _connection = psycopg2.connect(
        dbname=settings.DB_NAME,
        user=settings.DB_USER,
        password=settings.DB_PASS,
        host='postgres_oauth',
    )
    cursor = _connection.cursor()
    try:
        yield cursor
        _connection.commit()
    finally:
        cursor.close()
        _connection.close()


def create_user(
        email: str,
        password: str,
        first_name: Optional[str] = None,
        last_name: Optional[str] = None,
        role: Role = Role.worker,
) -> None:
    with connection() as conn:
        password = security.get_password_hash(password)
        conn.execute(
            'INSERT INTO users (public_id, email, first_name, last_name, password, role) '
            + f"VALUES ('{uuid4()}', '{email.lower()}', '{first_name}', '{last_name}', '{password}', '{role.value}');",
        )


def is_user_exist(email: str) -> bool:
    with connection() as conn:
        conn.execute(f"SELECT public_id FROM users WHERE email = '{email.lower()}';")
        res = conn.fetchone()
        return bool(res)


def get_user(
        email: str,
        password: str,
) -> User:
    with connection() as conn:
        conn.execute(
            f'SELECT public_id, email, first_name, last_name, password, role, is_active '
            + f"FROM users WHERE email = '{email.lower()}';"
        )
        res = conn.fetchone()
        if not res or not security.verify_password(password, res[4]):
            raise Exception('Not Found')
        return User(
            public_id=res[0],
            email=res[1],
            first_name=res[2],
            last_name=res[3],
            role=Role(res[5]),
            is_active=res[6],
        )


def update_user(public_id: str, **fields: str):
    if not fields:
        return
    set_statements = [f"{k} = '{v}'" for k, v in fields.items()]
    with connection() as conn:
        conn.execute(
            f"UPDATE users SET {','.join(set_statements)} WHERE public_id = '{public_id}'"
        )

