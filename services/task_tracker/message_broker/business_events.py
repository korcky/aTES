try:
    from models import Task
    from message_broker.kafka_imp import send
except ImportError:
    from ..models import Task
    from .kafka_imp import send


def task_assigned(task: Task):
    payload = {
        'event': 'TaskAssigned',
        'data': {'public_id': str(task.public_id), 'assignee_id': task.assignee_id},
    }
    send(topic='tasks_events', payload=payload)


def task_completed(task: Task):
    payload = {
        'event': 'TaskCompleted',
        'data': {'public_id': str(task.public_id), 'assignee_id': task.assignee_id},
    }
    send(topic='tasks_events', payload=payload)
