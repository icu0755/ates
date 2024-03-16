import uuid

from django.db import models
from django.contrib.auth.models import AbstractUser
from event_schema_registry import SchemaRegistry

from core.broker import Broker

ACCOUNT_ROLE_ADMIN = "admin"
ACCOUNT_ROLE_DEV = "developer"
ACCOUNT_ROLES = (
    (ACCOUNT_ROLE_ADMIN, ACCOUNT_ROLE_ADMIN),
    (ACCOUNT_ROLE_DEV, ACCOUNT_ROLE_DEV),
)


class Account(AbstractUser):
    role = models.CharField(max_length=40, choices=ACCOUNT_ROLES)
    public_id = models.UUIDField(default=uuid.uuid4)


def create_account(role):
    new_account = Account.objects.create(role=role)

    event = {
        "event": "AccountsAdded",
        "version": 1,
        "payload": {
            "public_id": str(new_account.public_id),
            "role": new_account.role,
        },
    }

    SchemaRegistry.validate_event(event, "accounts.added", version=1)

    Broker.send("accounts-stream", new_account)
    Broker.flush()
