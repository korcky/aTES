import random
from typing import Any

try:
    from db import update_user, create_task, update_task, create_transaction, get_task, create_payment
    from models import User, Role, TxType
    from message_broker import business_events
except ImportError:
    import business_events
    from ..db import update_user, create_task, update_task, create_transaction, get_task, create_payment
    from ..models import User, Role, TxType


def process_change_role(data: dict[str, Any]):
    public_id, role = data['public_id'], data['role']
    update_user(public_id=public_id, role=role)


def process_task_creation(data: dict[str, Any]):
    create_task(**data, fee=-random.randrange(10, 20), reward=random.randrange(20, 40))


def process_task_assignment(data: dict[str, Any]):
    public_id, assignee_id = data['public_id'], data['assignee_id']
    update_task(public_id=public_id, assignee_id=assignee_id)
    task = get_task(public_id=public_id)
    tx_id = create_transaction(
        user_id=task.assignee_id,
        description=f'assignment of task: {task.description}',
        tx_type=TxType.task_fee.value,
        debit=0,
        credit=-task.fee,
    )
    business_events.transaction_applied(tx_public_id=tx_id)


def process_task_completion(data: dict[str, Any]):
    public_id, assignee_id = data['public_id'], data['assignee_id']
    task = get_task(public_id=public_id)
    tx_id = create_transaction(
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
    tx_id = create_transaction(
        user_id=public_id,
        description=f'Withdraw balance to user',
        tx_type=TxType.yearns_payment,
        debit=0,
        credit=-balance,
    )
    business_events.transaction_applied(tx_public_id=tx_id)
    # There should be an interaction with some payment service
    payment_id = create_payment(transaction_id=tx_id, status='processing')
    business_events.payment_made(payment_public_id=payment_id, tx_public_id=tx_id)


EVENT_PROCESSOR_MAP = {
    'Accounts.RoleChanged': process_change_role,
    'Tasks.Created': process_task_creation,
    'Tasks.Completed': process_task_completion,
    'Tasks.Assigned': process_task_assignment,
    'Accounting.BillingCycleClosed': process_billing_cycle_closure,
}


def process_event(event: dict[str, Any]):
    processor_func = EVENT_PROCESSOR_MAP.get(event['event_name'])
    if processor_func:
        processor_func(data=event['data'])

