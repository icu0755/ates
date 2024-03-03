from task_tracker.core.models import Account


def on_message(message):
    if message["topic"] == "Accounts.Updated":
        account = Account.from_json(message["payload"])
        account.save()
    elif message["topic"] == "Accounts.Added":
        account = Account.from_json(message["payload"])
        account.save()
    print("from broker", message)
