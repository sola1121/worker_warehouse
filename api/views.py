import datetime

from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt   # 取消csrf
from django.http import JsonResponse

from account.models import History, User, Notification
from warehouse.models import InWarehouse, OutWareHouse, Warehouse, Classification, Sale

# Create your views here.

OK = "OK"

@login_required(login_url="/")
def api_current_user_history(request):
    """返回当前用户最近的NUM个数的历史"""
    NUM = 3
    if request.method == "POST":
        user_id = request.POST.get("user_id", '')
        if (not user_id) or str(user_id) != str(request.user.id):
            return JsonResponse({"back_msg": "用户信息获取失败."})
        time_list, msg_list = list(), list()
        histories = History.objects.filter(user_id=user_id)
        for info in histories.order_by("-create_date")[:NUM]:
            time_list.append(datetime.datetime.strftime(info.create_date, "%Y-%m-%d %H:%M:%S"))
            msg_list.append("{the_action_cn} {the_model_cn}".format(
                            the_action_cn=dict(History.ACTION_RECORD).get(info.action, "error"),
                            the_model_cn=dict(History.WARE_RECORD).get(info.affect_ware, "error")
                        ))
        return JsonResponse({"back_msg": OK, "time_list": time_list, "msg_list": msg_list})


@login_required(login_url="/")
def api_exists_inwarehouse_data(request):
    """"""
    pass    # TODO: 满足autocomplete功能, 具体的实现还没有想好