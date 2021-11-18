from event_schema_registry import generate_event

try:
    from models import Transaction, Balance
    from message_broker.kafka_imp import send
except ImportError:
    from ..models import Transaction, Balance
    from .kafka_imp import send


def transaction_created(transaction: Transaction):
    event = generate_event(
        'Accounting.TransactionCreated',
        version=1,
        producer='accounting',
        data=transaction.json_serializable(),
    )
    send(topic='accounting_stream', event=event)


def balance_created(balance: Balance):
    event = generate_event(
        'Accounting.Balance_created',
        version=1,
        producer='accounting',
        data=balance.json_serializable(),
    )
    send(topic='accounting_stream', event=event)
