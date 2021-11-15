from event_schema_registry import generate_event

try:
    from models import Task
    from message_broker.kafka_imp import send
except ImportError:
    from ..models import Task
    from .kafka_imp import send


def task_assigned(task: Task):
    event = generate_event(
        'Tasks.Assigned',
        version=1,
        producer='task_tracker',
        data={'public_id': str(task.public_id), 'assignee_id': str(task.assignee_id)},
    )
    send(topic='tasks_events', event=event)


def task_completed(task: Task):
    event = generate_event(
        'Tasks.Completed',
        version=1,
        producer='task_tracker',
        data={'public_id': str(task.public_id), 'assignee_id': str(task.assignee_id)},
    )
    send(topic='tasks_events', event=event)
