from logging import getLogger

from event_schema_registry import generate_event, validate

try:
    from message_broker.events_processor import process_event
    from message_broker.kafka_imp import consumer as _consumer, decode_event
except ImportError:
    from .events_processor import process_event
    from .kafka_imp import consumer as _consumer, decode_event


logger = getLogger(f'consumer')


def consume():
    consumer = _consumer('accounts_events', 'accounts_stream')
    for msg in consumer:
        try:
            event = decode_event(msg.value)
            if not validate(event, event_name=event['event_name'], version=event['event_version']):
                raise Exception('Invalid event schema')
            process_event(event=event)
        except Exception as e:
            logger.error(f'{msg}: {e}')


if __name__ == '__main__':
    try:
        consume()
    except Exception as e:
        logger.critical(e)
        exit(1)
