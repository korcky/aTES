import time
from logging import getLogger

from event_schema_registry import generate_event, validate

try:
    from message_broker.events_processor import process_event
    from message_broker.kafka_imp import consumer as _consumer, decode_event
except ImportError:
    from .events_processor import process_event
    from .kafka_imp import consumer as _consumer, decode_event


logger = getLogger(f'consumer')


def consume_message(message):
    event = decode_event(message.value)
    if not validate(event, event_name=event['event_name'], version=event['event_version']):
        raise Exception('Invalid event schema')
    process_event(event=event)


if __name__ == '__main__':
    retry_power = 0
    while True:
        try:
            consumer = _consumer('accounts_events', 'accounts_stream')
            for msg in consumer:
                try:
                    consume_message(msg)
                except Exception as e:
                    logger.error(f'{msg}: {e}')
                if retry_power != 0:
                    retry_power = 0
        except Exception as e:
            logger.critical(f'Error: {e}. Retry in {2**retry_power} seconds')
            time.sleep(2**retry_power)
            retry_power += 1

