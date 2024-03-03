from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponse, JsonResponse
from core.models import Account, Task, create_task, complete_task, assign_tasks


@login_required()
def create_task_view(request, *args, **kwargs):
    accounts = list(Account.objects.all())
    new_task = create_task(accounts)
    return JsonResponse(new_task.to_json(), status=201)


@login_required()
def complete_task_view(request, pk, *args, **kwargs):
    try:
        task = Task.objects.get(pk=pk)
    except Task.DoesNotExist:
        return JsonResponse({"error": "not found"}, status=404)
    complete_task(task)
    return JsonResponse(task.to_json(), status=200)


@login_required()
def assign_tasks_view(request, *args, **kwargs):
    accounts = list(Account.objects.all())
    assign_tasks(accounts)
    return HttpResponse(status=204)
