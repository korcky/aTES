from event_schema_registry import generate_event

try:
    from models import User, Role
    from message_broker.kafka_imp import send
except ImportError:
    from ..models import User, Role
    from .kafka_imp import send


def role_updated(public_id: str, new_role: Role):
    event = generate_event(
        'Accounts.RoleChanged',
        version=1,
        producer='oauth',
        data={'public_id': str(public_id), 'role': new_role.value}
    )
    send(topic='accounts_events', event=event)
