from django.core.management.base import BaseCommand
from django.db import transaction

from core.analytics import analytics
from core.models import Account, deduct_balance


class Command(BaseCommand):
    """
    Synchronous closing billing cycle
    """

    def handle(self, *args, **options):
        # The negative balance will be moved to the next day.
        accounts = Account.objects.filter(balance__gt=0)
        for account in accounts:
            with transaction.atomic():
                deduct_balance(account, "money withdrawn", account.balance)
                # do_payment()
        analytics.close_billing_cycle()
