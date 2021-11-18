from event_schema_registry import generate_event

try:
    from models import User
    from message_broker.kafka_imp import send
except ImportError:
    from .kafka_imp import send
    from ..models import User


def user_created(user: User):
    event = generate_event(
        'Accounts.Created',
        version=1,
        producer='oauth',
        data=user.json_serializable(),
    )
    send(topic='accounts_stream', event=event)


def user_updated(fields: dict[str, str]):
    event = generate_event(
        'Accounts.Updated',
        version=1,
        producer='oauth',
        data=fields,
    )
    send(topic='accounts_stream', event=event)
