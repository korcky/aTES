import json
from typing import Any

from kafka import KafkaProducer, KafkaConsumer


def producer() -> KafkaProducer:
    return KafkaProducer(bootstrap_servers='host.docker.internal:9093')


def consumer(*topics: str) -> KafkaConsumer:
    return KafkaConsumer(*topics, bootstrap_servers='host.docker.internal:9093')


def encode_event(payload: dict[str, Any]) -> bytes:
    return json.dumps(payload).encode('utf8')


def decode_event(payload: bytes) -> dict[str, Any]:
    return json.loads(payload.decode('utf8'))


def send(topic: str, event: dict[str, Any]) -> None:
    producer().send(topic, encode_event(event))
