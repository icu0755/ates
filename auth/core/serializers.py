from rest_framework import serializers

from core.models import Account
from core.broker import notify


class AccountSerializer(serializers.ModelSerializer):
    def __init__(self, instance=None, **kwargs):
        self._old_data = {}
        if instance:
            self._old_data = instance.to_json()
        super().__init__(instance, **kwargs)

    def save(self, **kwargs):
        account = super().save(**kwargs)
        notify("Accounts.Updated", account.to_json())  # CUD
        if self._old_data and self._old_data["role"] != account.role:
            notify("Accounts.RoleChanged", account.to_json())  # BE
        return account

    class Meta:
        model = Account
        fields = (
            "id",
            "role",
        )
