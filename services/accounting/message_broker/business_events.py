from event_schema_registry import generate_event

try:
    from models import Task
    from message_broker.kafka_imp import send
except ImportError:
    from ..models import Task
    from .kafka_imp import send


def transaction_applied(tx_public_id):
    event = generate_event(
        'Accounting.TransactionApplied',
        version=1,
        producer='accounting',
        data={'public_id': str(tx_public_id)},
    )
    send(topic='accounting_events', event=event)


def billing_cycle_closed(user_public_id, balance):
    event = generate_event(
        'Accounting.BillingCycleClosed',
        version=1,
        producer='scheduler',
        data={'public_id': str(user_public_id), 'balance': int(balance)},
    )
    send(topic='billing_cycle_events', event=event)


def payment_made(payment_public_id, tx_public_id):
    event = generate_event(
        'Accounting.PaymentMade',
        version=1,
        producer='accounting',
        data={'public_id': str(payment_public_id), 'transaction_id': str(tx_public_id)},
    )
    send(topic='accounting_events', event=event)
