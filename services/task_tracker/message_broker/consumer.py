from logging import getLogger

try:
    from message_broker.events_processor import process_event
    from message_broker.kafka_imp import consumer as _consumer, decode_payload
except ImportError:
    from .events_processor import process_event
    from .kafka_imp import consumer as _consumer, decode_payload


logger = getLogger(f'consumer')


def consume():
    consumer = _consumer('accounts_events', 'accounts_stream')
    for msg in consumer:
        try:
            payload = decode_payload(msg.value)
            process_event(payload=payload)
        except Exception as e:
            logger.error(f'{msg}: {e}')


if __name__ == '__main__':
    try:
        consume()
    except Exception as e:
        logger.critical(e)
        exit(1)
