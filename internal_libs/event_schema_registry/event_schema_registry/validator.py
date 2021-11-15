import re
import json
import pathlib
import os.path
from datetime import datetime, timezone
from typing import Any
from uuid import uuid4

import jsonschema

SCHEMAS_PATH = os.path.join(
    pathlib.Path(__file__).parent.resolve(),
    'schemas',
)


def generate_event(
        event_name: str,
        version: int,
        producer: str,
        data: dict[str, Any],
) -> dict[str, Any]:
    return {
        'event_id': str(uuid4()),
        'event_version': version,
        'event_name': event_name,
        'event_time': str(datetime.now(tz=timezone.utc)),
        'producer': producer,
        'data': data,
    }


def _format_dict_name(name: str) -> str:
    parts = re.findall('[A-Z][^A-Z]*', name)
    return '_'.join(part.lower() for part in parts)


def _retrieve_schema(
        event_name: str,
        version: int,
) -> dict[str, Any]:
    domain, event = event_name.split('.')
    schema_path = os.path.join(
        SCHEMAS_PATH,
        _format_dict_name(domain),
        _format_dict_name(event),
        f'{version}.json',
    )
    with open(schema_path, 'r') as schema_file:
        return json.load(schema_file)


def validate(
        event: dict[str, Any],
        event_name: str,
        version: int,
) -> bool:
    try:
        schema = _retrieve_schema(
            event_name=event_name,
            version=version,
        )
        jsonschema.validate(event, schema=schema)
        return True
    except FileNotFoundError:
        return False
    except jsonschema.ValidationError:
        return False
