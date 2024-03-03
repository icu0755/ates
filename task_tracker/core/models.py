import random

from django.db import models
from django.contrib.auth.models import AbstractUser


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

    def to_json(self):
        return {
            "id": self.pk,
            "assignee": self.role,
        }


class Task(models.Model):
    assignee = models.ForeignKey(Account, on_delete=models.CASCADE)
    status = models.CharField(max_length=40, choices=TASK_STATUSES)

    def to_json(self):
        return {
            "id": self.pk,
            "assignee": self.assignee.pk,
            "status": self.status,
        }


def notify(topic, payload):
    pass


def create_task(accounts):
    assignee = random.choice(accounts)
    new_task = Task.objects.create(
        assignee=assignee,
        status=TASK_STATUS_OPEN,
    )
    notify("Tasks.Added", new_task.to_json())  # BE
    return new_task


def complete_task(task):
    task.status = TASK_STATUS_COMPLETED
    task.save()
    notify("Tasks.Completed", task.to_json())  # BE


def assign_tasks(accounts):
    tasks = Task.objects.all()
    for task in tasks:
        task.assignee = random.choice(accounts)
        task.save()
        notify("Tasks.Assigned", task.to_json())  # BE
