import json

from django.conf import settings
from kafka import KafkaProducer


def json_serializer(v):
    return json.dumps(v).encode()


class Broker:
    producer = None

    @classmethod
    def send(cls, topic, payload):
        producer = cls.get_producer()
        producer.send(topic, payload)

    @classmethod
    def flush(cls):
        producer = cls.get_producer()
        producer.flush()

    @classmethod
    def get_producer(cls):
        if cls.producer is None:
            cls.producer = KafkaProducer(
                value_serializer=json_serializer, bootstrap_servers=settings.BROKER_URL
            )
        return cls.producer
