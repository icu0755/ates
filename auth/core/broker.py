import msgpack
from django.conf import settings
from kafka import KafkaProducer

producer = KafkaProducer(
    value_serializer=msgpack.dumps, bootstrap_servers=settings.BROKER_URL
)


def notify(topic, payload):
    producer.send(topic, payload)
