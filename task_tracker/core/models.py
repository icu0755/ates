import random

from django.db import models
from django.contrib.auth.models import AbstractUser

from core.broker import Broker
from event_schema_registry import SchemaRegistry

ACCOUNT_ROLE_ADMIN = "admin"
ACCOUNT_ROLE_DEV = "developer"
ACCOUNT_ROLES = (
    (ACCOUNT_ROLE_ADMIN, ACCOUNT_ROLE_ADMIN),
    (ACCOUNT_ROLE_DEV, ACCOUNT_ROLE_DEV),
)

TASK_STATUS_OPEN = "open"
TASK_STATUS_COMPLETED = "completed"
TASK_STATUSES = (
    (TASK_STATUS_OPEN, TASK_STATUS_OPEN),
    (TASK_STATUS_COMPLETED, TASK_STATUS_COMPLETED),
)


class Account(AbstractUser):
    role = models.CharField(max_length=40, choices=ACCOUNT_ROLES)
    public_id = models.UUIDField()


class Task(models.Model):
    description = models.CharField()
    assignee = models.ForeignKey(Account, on_delete=models.CASCADE)
    status = models.CharField(max_length=40, choices=TASK_STATUSES)
    public_id = models.UUIDField()


def create_task(accounts):
    assignee = random.choice(accounts)
    new_task = Task.objects.create(
        assignee=assignee,
        status=TASK_STATUS_OPEN,
    )
    event = {
        "event": "TasksAdded",
        "version": 1,
        "payload": {
            "public_id": str(new_task.public_id),
            "assignee_id": str(assignee.public_id),
            "description": new_task.description,
        },
    }

    SchemaRegistry.validate_event(event, "tasks.added", version=1)

    Broker.send("tasks-lifecycle", event)

    return new_task


def complete_task(task):
    task.status = TASK_STATUS_COMPLETED
    task.save()

    event = {
        "event": "TasksCompleted",
        "version": 1,
        "payload": {
            "public_id": str(task.public_id),
            "assignee_id": str(task.assignee.public_id),
        },
    }

    SchemaRegistry.validate_event(event, "tasks.completed", version=1)

    Broker.send("tasks-lifecycle", event)


def assign_tasks(accounts):
    tasks = Task.objects.all()
    for task in tasks:
        task.assignee = random.choice(accounts)
        task.save()

        event = {
            "event": "TasksAssigned",
            "version": 1,
            "payload": {
                "public_id": str(task.public_id),
                "assignee_id": task.assignee.public_id,
            },
        }

        SchemaRegistry.validate_event(event, "tasks.assigned", version=1)

        # batching is done internally
        Broker.send("tasks-lifecycle", event)

    Broker.flush()
