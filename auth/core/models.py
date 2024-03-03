from django.db import models
from django.contrib.auth.models import AbstractUser

ACCOUNT_ROLE_ADMIN = "admin"
ACCOUNT_ROLE_DEV = "developer"
ACCOUNT_ROLES = (
    (ACCOUNT_ROLE_ADMIN, ACCOUNT_ROLE_ADMIN),
    (ACCOUNT_ROLE_DEV, ACCOUNT_ROLE_DEV),
)


class Account(AbstractUser):
    role = models.CharField(max_length=40, choices=ACCOUNT_ROLES)

    def to_json(self):
        return {
            "id": self.pk,
            "assignee": self.role,
        }


def create_account(role):
    new_account = Account.objects.create(role=role)
    notify("Accounts.Added", new_account.to_json())  # BE


def notify(topic, payload):
    pass
