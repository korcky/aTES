from typing import Any

try:
    from db import create_or_update_user
    from models import User, Role
except ImportError:
    from ..db import create_or_update_user
    from ..models import User, Role


def process_change_role(data: dict[str, Any]):
    public_id, role = data['public_id'], data['role']
    create_or_update_user(public_id=public_id, role=role)


def process_user_stream_event(data: dict[str, Any]):
    create_or_update_user(**data)


EVENT_PROCESSOR_MAP = {
    'Accounts.RoleChanged': process_change_role,
    'Accounts.Created': process_user_stream_event,
    'Accounts.Updated': process_user_stream_event,
}


def process_event(event: dict[str, Any]):
    processor_func = EVENT_PROCESSOR_MAP.get(event['event_name'])
    if processor_func:
        processor_func(data=event['data'])
