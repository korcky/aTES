from event_schema_registry import generate_event

try:
    from models import Task
    from message_broker.kafka_imp import send
except ImportError:
    from ..models import Task
    from .kafka_imp import send


def task_created(task: Task):
    event = generate_event(
        'Tasks.Created',
        version=1,
        producer='task_tracker',
        data={'public_id': str(task.public_id), 'description': task.description},
    )
    send(topic='tasks_stream', event=event)
