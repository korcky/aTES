import random
from typing import Any

try:
    import db
    from models import User, Role, TxType
    from message_broker import business_events
except ImportError:
    import business_events
    from .. import db
    from ..models import User, Role, TxType


def process_change_role(data: dict[str, Any]):
    public_id, role = data['public_id'], data['role']
    db.create_or_update_user(public_id=public_id, role=role)


def process_user_stream_event(data: dict[str, Any]):
    db.create_or_update_user(**data)


def process_task_creation(data: dict[str, Any]):
    db.create_task(**data, fee=-random.randrange(10, 20), reward=random.randrange(20, 40))


def process_task_assignment(data: dict[str, Any]):
    public_id, assignee_id = data['public_id'], data['assignee_id']
    db.update_task(public_id=public_id, assignee_id=assignee_id)
    task = db.get_task(public_id=public_id)
    tx_id = db.create_transaction(
        user_id=task.assignee_id,
        description=f'assignment of task: {task.description}',
        tx_type=TxType.task_fee.value,
        debit=0,
        credit=-task.fee,
    )
    business_events.transaction_applied(tx_public_id=tx_id)


def process_task_completion(data: dict[str, Any]):
    public_id, assignee_id = data['public_id'], data['assignee_id']
    task = db.get_task(public_id=public_id)
    tx_id = db.create_transaction(
        user_id=assignee_id,
        description=f'reward for task: {task.description}',
        tx_type=TxType.task_reward.value,
        debit=task.reward,
        credit=0,
    )
    business_events.transaction_applied(tx_public_id=tx_id)


def process_billing_cycle_closure(data: dict[str, Any]):
    public_id, balance = data['public_id'], data['balance']
    if balance <= 0:
        return
    tx_id = db.create_transaction(
        user_id=public_id,
        description=f'Withdraw balance to user',
        tx_type=TxType.yearns_payment,
        debit=0,
        credit=-balance,
    )
    business_events.transaction_applied(tx_public_id=tx_id)
    # There should be an interaction with some payment service
    payment_id = db.create_payment(transaction_id=tx_id, status='processing')
    business_events.payment_made(payment_public_id=payment_id, tx_public_id=tx_id)
    # there should be request to some another microservice (or business event)
    # with user email and text about payment, that user will receive


EVENT_PROCESSOR_MAP = {
    'Accounts.RoleChanged': process_change_role,
    'Tasks.Created': process_task_creation,
    'Tasks.Completed': process_task_completion,
    'Tasks.Assigned': process_task_assignment,
    'Accounting.BillingCycleClosed': process_billing_cycle_closure,
    'Accounts.Created': process_user_stream_event,
    'Accounts.Updated': process_user_stream_event,
}


def process_event(event: dict[str, Any]):
    processor_func = EVENT_PROCESSOR_MAP.get(event['event_name'])
    if processor_func:
        processor_func(data=event['data'])

