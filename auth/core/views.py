from django.http.response import JsonResponse
from core.models import Account, ACCOUNT_ROLE_DEV, create_account
from core.serializers import AccountSerializer


def create_account_view(request, *args, **kwargs):
    new_account = create_account(role=ACCOUNT_ROLE_DEV)
    return JsonResponse(new_account.to_json(), status=201)


def save_account_view(request, pk, **kwargs):
    try:
        account = Account.objects.get(pk=pk)
    except Account.DoesNotExist:
        return JsonResponse({"error": "not_found"}, status=404)

    serializer = AccountSerializer(instance=account, data=request.data)
    serializer.is_valid(raise_exception=True)
    account = serializer.save()

    return JsonResponse(account.to_json(), status=200)
