import json

from django.conf import settings
from django.core.management.base import BaseCommand
from kafka import KafkaConsumer

from event_schema_registry import SchemaRegistry

from core.analytics import analytics
from core.models import (
    Account,
    get_or_create_task,
    deduct_balance,
    add_balance,
)


def json_deserializer(v):
    return json.loads(v.decode())


class Command(BaseCommand):
    def handle(self, *args, **options):
        consumer = KafkaConsumer(
            "accounts-stream",
            "tasks-lifecycle",
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

            elif event["name"] == "TasksAdded" and event["version"] == 1:
                SchemaRegistry.validate_event(event, "tasks.added", version=1)
                account = Account.objects.get(public_id=event["payload"]["assignee_id"])
                task = get_or_create_task(
                    public_id=event["payload"]["public_id"],
                    description=event["payload"]["description"],
                )
                deduct_balance(account, "task assigned", task.assign_cost)
                analytics.task_assigned(account, task.assign_cost)

            elif event["name"] == "TasksAssigned" and event["version"] == 1:
                SchemaRegistry.validate_event(event, "tasks.assigned", version=1)
                task = get_or_create_task(
                    public_id=event["payload"]["public_id"],
                )
                account = Account.objects.get(public_id=event["payload"]["assignee_id"])
                deduct_balance(account, "task assigned", task.assign_cost)
                analytics.task_assigned(account, task.assign_cost)

            elif event["name"] == "TasksCompleted" and event["version"] == 1:
                SchemaRegistry.validate_event(event, "tasks.completed", version=1)
                task = get_or_create_task(
                    public_id=event["payload"]["public_id"],
                )
                account = Account.objects.get(public_id=event["payload"]["assignee_id"])
                add_balance(account, "task completed", task.complete_cost)
                analytics.task_completed(account, task.complete_cost)
