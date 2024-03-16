import json

from django.conf import settings
from django.core.management.base import BaseCommand
from kafka import KafkaConsumer

from event_schema_registry import SchemaRegistry

from core.models import Account


def json_deserializer(v):
    return json.loads(v.decode())


class Command(BaseCommand):
    def handle(self, *args, **options):
        consumer = KafkaConsumer(
            "accounts-stream",
            value_deserializer=json_deserializer,
            bootstrap_servers=settings.BROKER_URL,
        )
        for msg in consumer:
            event = msg.value
            if event["name"] == "AccountsAdded" and event["version"] == 1:
                SchemaRegistry.validate_event(event, "accounts.added", version=1)
                Account.objects.create(
                    role=event["payload"]["role"],
                    public_id=event["payload"]["public_id"],
                )
