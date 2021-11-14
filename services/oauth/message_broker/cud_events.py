try:
    from models import User
    from message_broker.kafka_imp import send
except ImportError:
    from .kafka_imp import send
    from ..models import User


def user_created(user: User):
    payload = {
        'event': 'UserCreated',
        'data': user.json_serializable(),
    }
    send(topic='accounts_stream', payload=payload)


def user_updated(fields: dict[str, str]):
    payload = {
        'event': 'UserUpdated',
        'data': fields,
    }
    send(topic='accounts_stream', payload=payload)
