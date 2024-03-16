import random

from django.contrib.auth.models import AbstractUser
from django.db import models


ACCOUNT_ROLE_ADMIN = "admin"
ACCOUNT_ROLE_DEV = "developer"
ACCOUNT_ROLES = (
    (ACCOUNT_ROLE_ADMIN, ACCOUNT_ROLE_ADMIN),
    (ACCOUNT_ROLE_DEV, ACCOUNT_ROLE_DEV),
)


class Account(AbstractUser):
    role = models.CharField(max_length=40, choices=ACCOUNT_ROLES)
    public_id = models.UUIDField()
    balance = models.IntegerField(default=0)


def create_assign_cost():
    return random.randint(10, 20)


def create_complete_cost():
    return random.randint(20, 40)


class Task(models.Model):
    description = models.CharField(default="")
    public_id = models.UUIDField()
    assign_cost = models.IntegerField(default=create_assign_cost)
    complete_cost = models.IntegerField(default=create_assign_cost)


def get_or_create_task(public_id, description=None):
    """
    Task is eventually consistent. The description can come later.
    """
    task, is_created = Task.objects.get_or_create(
        public_id=public_id,
        defaults={
            "description": description or "",
            # assign_cost calculated automatically
            # complete_cost calculated automatically
        },
    )
    if not is_created and description:
        task.description = description
        task.save(updated_fields=["description"])
    return task


class Transaction(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    description = models.CharField()
    credit = models.IntegerField(default=0)
    debit = models.IntegerField(default=0)


def add_balance(account, description, amount):
    account.balance += amount
    account.save(update_fields=["balance"])
    Transaction.objects.create(
        account=account,
        description=description,
        debit=amount,
    )


def deduct_balance(account, description, amount):
    account.balance -= amount
    account.save(update_fields=["balance"])
    Transaction.objects.create(
        account=account,
        description=description,
        credit=amount,
    )
