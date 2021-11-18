import random
from typing import Any

try:
    import db
    from models import User, Role, TxType
except ImportError:
    from .. import db
    from ..models import User, Role, TxType


def process_change_role(data: dict[str, Any]):
    public_id, role = data['public_id'], data['role']
    db.create_or_update_user(public_id=public_id, role=role)


def process_user_stream_event(data: dict[str, Any]):
    db.create_or_update_user(**data)


def process_task_creation(data: dict[str, Any]):
    db.create_task(**data, fee=-random.randrange(10, 20), reward=random.randrange(20, 40))


def process_transaction_creation(data: dict[str, Any]):
    db.create_transaction(**data)


def process_balance_creation(data: dict[str, Any]):
    db.create_transaction(**data)


EVENT_PROCESSOR_MAP = {
    'Accounts.RoleChanged': process_change_role,
    'Tasks.Created': process_task_creation,
    'Accounts.Created': process_user_stream_event,
    'Accounts.Updated': process_user_stream_event,
    'Accounting.TransactionCreated': process_transaction_creation,
    'Accounting.BalanceCreated': process_balance_creation,
}


def process_event(event: dict[str, Any]):
    processor_func = EVENT_PROCESSOR_MAP.get(event['event_name'])
    if processor_func:
        processor_func(data=event['data'])

