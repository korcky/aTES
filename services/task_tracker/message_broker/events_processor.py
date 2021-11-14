from typing import Any

try:
    from db import update_user
    from models import User, Role
except ImportError:
    from ..db import update_user
    from ..models import User, Role


def process_change_role(data: dict[str, Any]):
    public_id, role = data['public_id'], data['role']
    update_user(public_id=public_id, role=role)


EVENT_PROCESSOR_MAP = {
    'RoleChanged': process_change_role,
}


def process_event(payload: dict[str, Any]):
    processor_func = EVENT_PROCESSOR_MAP.get(payload['event'])
    if processor_func:
        processor_func(data=payload['data'])
