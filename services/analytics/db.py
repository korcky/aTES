from contextlib import contextmanager
from datetime import datetime, timezone, date, timedelta
from typing import Optional
from uuid import UUID, uuid4

import psycopg2

import settings
from models import Role, User, Task, Status, Transaction, TxType, Balance


@contextmanager
def connection():
    _connection = psycopg2.connect(
        dbname=settings.DB_NAME,
        user=settings.DB_USER,
        password=settings.DB_PASS,
        host='analytics_postgres',
    )
    cursor = _connection.cursor()
    try:
        yield cursor
        _connection.commit()
    finally:
        cursor.close()
        _connection.close()


def _format_value(value) -> str:
    if isinstance(value, str):
        return f"'{value}'"
    return str(value)


def create_or_update_user(public_id: str, **fields: str):
    with connection() as conn:
        conn.execute(f"SELECT EXISTS(SELECT 1 FROM users WHERE public_id = '{public_id}')")
        if conn.fetchone()[0]:
            if not fields:
                return
            set_statements = [f"{k} = '{v}'" for k, v in fields.items()]
            conn.execute(f"UPDATE users SET {','.join(set_statements)} WHERE public_id = '{public_id}';")
        else:
            fields['public_id'] = public_id
            fields_names = fields.keys()
            fields_values = [_format_value(fields[name]) for name in fields_names]
            conn.execute(f"INSERT INTO users ({', '.join(fields_names)}) VALUES ({', '.join(fields_values)})")


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


def create_task(public_id, title, jira_id, description, fee, reward) -> Task:
    with connection() as conn:
        conn.execute(
            'INSERT INTO tasks (public_id, title, jira_id, description, status) '
            + f"VALUES ('{public_id}', '{title}', '{jira_id}', '{description}', '{Status.open.value}', {fee}, {reward});",
        )
        return Task(
            public_id=public_id,
            assignee_id=None,
            title=title,
            jira_id=jira_id,
            description=description,
            status=Status.open,
            fee=fee,
            reward=reward,
        )


def get_task(public_id) -> Task:
    with connection() as conn:
        conn.execute(
            'SELECT public_id, assignee_id, title, jira_id, description, status, fee, reward '
            + 'FROM tasks '
            + f"WHERE public_id = '{public_id}' "
        )
        task = conn.fetchone()
        return Task(
            public_id=task[0],
            assignee_id=task[1],
            title=task[2],
            jira_id=task[3],
            description=task[4],
            status=Status(task[5]),
            fee=task[6],
            reward=task[7],
        )


def update_task(public_id, assignee_id):
    with connection() as conn:
        conn.execute(f"UPDATE tasks SET assignee_id = '{assignee_id}' WHERE public_id = '{public_id}'")


def get_management_yearns_for_today() -> int:
    with connection() as conn:
        conn.execute(
            'SELECT -1 * ( SUM(debit) + SUM(credit) ) '
            + 'FROM transactions '
            + f"WHERE (type = '{TxType.task_fee}' OR type = '{TxType.task_reward}') AND created_at >= NOW()::DATE;"
        )
        res = conn.fetchone()
        return res[0]


def create_transaction(**fields):
    fields_names = fields.keys()
    fields_values = [_format_value(fields[name]) for name in fields_names]
    with connection() as conn:
        conn.execute(
            f"INSERT INTO transactions ({', '.join(fields_names)}) VALUES ({', '.join(fields_values)})"
        )


def create_balance(**fields):
    fields_names = fields.keys()
    fields_values = [_format_value(fields[name]) for name in fields_names]
    with connection() as conn:
        conn.execute(
            f"INSERT INTO balances ({', '.join(fields_names)}) VALUES ({', '.join(fields_values)})"
        )


def get_transactions(user_id: Optional[str] = None) -> list[Transaction]:
    with connection() as conn:
        conn.execute(
            'SELECT public_id, user_id, description, type, debit, credit, created_at '
            + 'FROM transactions ' + (f"WHERE user_id = '{user_id}'" if user_id else '')
            + 'ORDER BY created_at DESC;'
        )
        res = conn.fetchall()
        return [
            Transaction(*tx)
            for tx in res
        ]


def get_most_expensive_tasks():
    now = datetime.now(tz=timezone.utc)
    with connection() as conn:
        conn.execute(
            f"SELECT "
            + f"MAX(ABS(credit)) FILTER(WHERE created_at >= '{now - timedelta(days=30)}'), "
            + f"MAX(ABS(credit)) FILTER(WHERE created_at >= '{now - timedelta(days=7)}'), "
            + f"MAX(ABS(credit)) FILTER(WHERE created_at >= '{now - timedelta(days=1)}') "
            + f" FROM transactions "
            + f"WHERE type = '{TxType.task_reward}' AND created_at >= '{now - timedelta(days=30)}';",
        )
        for_month, for_week, for_day = conn.fetchone()
        return for_month, for_week, for_day


def get_balances(user_id: str) -> list[Balance]:
    with connection() as conn:
        conn.execute(
            'SELECT for_date, balance '
            + 'FROM balances '
            + f"WHERE user_id = '{user_id}' "
            + 'ORDER BY for_date DESC;'
        )
        balances = [
            Balance(user_id=user_id, for_date=row[0], balance=row[1])
            for row in conn.fetchall()
        ]
        conn.execute(
            'SELECT ( SUM(debit) + SUM(credit) ) '
            + 'FROM transactions '
            + f"WHERE user_id = '{user_id}' "
            + (f"AND created_at >= '{balances[0].for_date}';" if balances else '')
        )
        res = conn.fetchone()
        if balances:
            if res[0]:
                balances[0].balance += res[0]
        else:
            balances = [
                Balance(
                    user_id=user_id,
                    for_date=datetime.now(tz=timezone.utc).date(),
                    balance=res[0] if res[0] else 0,
                ),
            ]
        return balances


def calculate_new_balances(today: date) -> list[Balance]:
    previous_day = today - timedelta(days=1)
    with connection() as conn:
        conn.execute(f"SELECT user_id, balance FROM balances WHERE for_date = '{previous_day}';")
        balances = {row[0]: row[1] for row in conn.fetchall()}
        conn.execute(
            'SELECT user_id, ( SUM(debit) + SUM(credit) ) FROM transactions '
            + f"WHERE created_at >= '{previous_day}' "
            + 'GROUP BY user_id;'
        )
        balances_changes = {row[0]: row[1] for row in conn.fetchall()}
        for user_id, balance_change in balances_changes.items():
            prev_balance = balances.get(user_id, 0)
            balances[user_id] = prev_balance + balance_change
        return [
            Balance(
                user_id=user_id,
                balance=balance,
                for_date=today,
            )
            for user_id, balance in balances.items()
        ]


def get_below_zero_worker_count() -> int:
    with connection() as conn:
        conn.execute(f'SELECT user_id, balance FROM balances WHERE for_date = NOW()::DATE;')
        balances = {row[0]: row[1] for row in conn.fetchall()}
        conn.execute(
            'SELECT user_id, ( SUM(debit) + SUM(credit) ) FROM transactions '
            + f'WHERE created_at >= NOW()::DATE '
            + 'GROUP BY user_id;'
        )
        balances_changes = {row[0]: row[1] for row in conn.fetchall()}
        for user_id, balance_change in balances_changes.items():
            prev_balance = balances.get(user_id, 0)
            balances[user_id] = prev_balance + balance_change
        return sum(balance < 0 for balance in balances.values())


def create_balances(balances: list[Balance]):
    values = [f"('{b.user_id}', '{b.for_date}', '{b.balance}')" for b in balances]
    values = ', '.join(values)
    with connection() as conn:
        conn.execute(
            f'INSERT INTO balances (user_id, for_date, balance) VALUES {values};'
        )


def create_payment(transaction_id, status):
    public_id = uuid4()
    with connection() as conn:
        conn.execute(
            'INSERT INTO payments (public_id, transaction_id, status) '
            + f"VALUES ('{public_id}', '{transaction_id}', '{status}');",
        )
        return public_id
