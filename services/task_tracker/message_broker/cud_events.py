try:
    from models import Task
    from message_broker.kafka_imp import send
except ImportError:
    from ..models import Task
    from .kafka_imp import send


def task_created(task: Task):
    payload = {
        'event': 'TaskCreated',
        'data': task.json_serializable(),
    }
    send(topic='tasks_stream', payload=payload)
