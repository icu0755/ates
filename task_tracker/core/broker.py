import msgpack
from django.conf import settings
from kafka import KafkaConsumer, KafkaProducer

from core.models import Account

producer = KafkaProducer(
    value_serializer=msgpack.dumps, bootstrap_servers=settings.BROKER_URL
)
consumer = KafkaConsumer(
    "Accounts.Updated",
    "Accounts.Added",
    value_deserializer=msgpack.loads,
    bootstrap_servers=settings.BROKER_URL,
)


def notify(topic, payload):
    producer.send(topic, payload)


def on_message(message):
    if message.headers["topic"] == "Accounts.Updated":
        account = Account.from_json(message["payload"])
        account.save()
    elif message.headers["topic"] == "Accounts.Added":
        account = Account.from_json(message.value)
        account.save()


for msg in consumer:
    print(msg.headers, msg.value)
    on_message(msg)
