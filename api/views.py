from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse

from account.models import History

# Create your views here.

OK = "OK"

@login_required(login_url="/")
def api_current_user_history(request):
    if request.method == "POST":
        content_list = list()
        histories = History.objects.filter(user_id=request.user.id)
        for history in histories.order_by("-create_date"):
            content_list.append(history.get_record())
        return JsonResponse({"err_msg": OK, "content": content_list})