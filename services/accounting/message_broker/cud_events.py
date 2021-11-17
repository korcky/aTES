from event_schema_registry import generate_event

try:
    from models import Task
    from message_broker.kafka_imp import send
except ImportError:
    from ..models import Task
    from .kafka_imp import send


def task_created(task: Task):
    # todo: BRUH, NOPE
    event = generate_event(
        'Tasks.Created',
        version=2,
        producer='task_tracker',
        data={
            'public_id': str(task.public_id),
            'title': task.title,
            'jira_id': task.jira_id,
            'description': task.description,
        },
    )
    send(topic='tasks_stream', event=event)
