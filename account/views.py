import logging
import datetime
import collections

import pytz
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator

from .models import User, History
from warehouse.models import InWarehouse, OutWareHouse, Warehouse, Sale, Classification

# Create your views here.

PER_PAGE_HISTORY = 20
TZ = pytz.timezone("Asia/Shanghai")

### 用户账户管理 ###

def account_login(request):
    """账户登录"""
    if request.user.is_authenticated:
        return redirect("/index")
    if request.method == "POST":
        uname = request.POST.get("loginUsername", None)
        upass = request.POST.get("loginPassword", None)
        if not all([uname, upass]):
            return render(request, "app_account/login.html", {"error_msg": "账户名或密码为空"})
        if not User.objects.filter(username=uname):
            return render(request, "app_account/login.html", {"error_msg": "该账户不存在"})
        else:
            user = authenticate(username=uname, password=upass)
            if not user:
                return render(request, "app_account/login.html", {"error_msg": "密码错误"})
            if user.is_active:
                login(request, user)
                return render(request, "app_index/index.html", {"active_navbar": "index"})
            else:
                return render(request, "app_account/login.html", {"error_msg": "账户被禁用"})
    return render(request, "app_account/login.html")


def account_logout(request):
    """账户登出"""
    logout(request)
    return render(request, "app_account/login.html")


@login_required(login_url="/")
def account_change_password(request):
    """账户更改自己的密码"""
    if request.method == "POST":
        old_pass = request.POST.get("oldPassword", None)
        new_pass1 = request.POST.get("newPassword1", None)
        new_pass2 = request.POST.get("newPassword2", None)
        if not all([old_pass, new_pass1, new_pass2]):
            return render(request, "app_account/change_password.html", {"error_msg": "输入存在空"})
        user = request.user
        if not user.check_password(old_pass):
            return render(request, "app_account/change_password.html", {"error_msg": "旧密码不匹配"})
        if new_pass1 != new_pass2:
            return render(request, "app_account/change_password.html", {"error_msg": "新密码不一致"})
        user.set_password(new_pass1)
        user.save()
        logout(request)
        return redirect("/")
    return render(request, "app_account/change_password.html")


### 用于history处理GET请求参数 ###

class RequestQueryHandler:
    """处理GET请求参数"""
    def __init__(self, request):
        self.username = request.GET.get("userName", '')
        self.fullname = request.GET.get("fullName", '')
        self.warename = request.GET.get("wareName", '')
        self.action = request.GET.get("action", '')
        self._time_deal(request)
    
    def _time_deal(self, request):
        start_time = request.GET.get("startTime", '')
        end_time = request.GET.get("endTime", '')
        self.origin_start_time, self.origin_end_time = start_time, end_time
        try:
            if start_time:
                trans_time = datetime.datetime.strptime(start_time, "%Y-%m-%d") - datetime.timedelta(days=1)
                self.start_time = datetime.datetime(trans_time.year, trans_time.month, trans_time.day, tzinfo=TZ)
            else:
                self.start_time = datetime.datetime(1970, 1, 1, 0, 0, tzinfo=TZ)
            if end_time:
                trans_time = datetime.datetime.strptime(end_time, "%Y-%m-%d") + datetime.timedelta(days=1)
                self.end_time = datetime.datetime(trans_time.year, trans_time.month, trans_time.day, tzinfo=TZ)
            else:
                self.end_time = datetime.datetime.now(TZ)
            if start_time and end_time:
                if self.start_time > self.end_time:
                    self.start_time, self.end_time = self.end_time, self.start_time
        except Exception as ex:
            logging.error(ex)
            return render(request, "exceptions/500.html", status=500)


### 用户历史管理 ###

@login_required(login_url="/")
def history(request, page=1):
    """用户历史信息的查询"""
    request_query = RequestQueryHandler(request)
    username, fullname, warename, action = (request_query.username, request_query.fullname, 
                                            request_query.warename, request_query.action)
    start_time, end_time = request_query.start_time, request_query.end_time
    users = User.objects.filter(username__icontains=username, full_name__icontains=fullname)
    query_string = dict(user_id__in=[uid[0] for uid in users.values_list("id")], 
                        create_date__gte=start_time, create_date__lte=end_time)
    if warename:
        query_string["affect_ware"] = warename
    if action:
        query_string["action"] = action
    histories = History.objects.filter(**query_string)
    paginator = Paginator(histories.order_by("-create_date"), PER_PAGE_HISTORY)
    if int(page) not in list(paginator.page_range):
        return redirect("/history/")
    pagetor = paginator.get_page(page)
    return render(request, 
                  "app_account/history.html",
                  {"active_navbar": "history",
                   "pagetor": pagetor,
                   "username": username,
                   "fullname": fullname,
                   "warename": warename,
                   "action": action,
                   "start_time": request_query.origin_start_time,
                   "end_time": request_query.origin_end_time,
                   "select_warehouse_tag": collections.OrderedDict(History.WARE_RECORD),
                   "select_action_tag": collections.OrderedDict(History.ACTION_RECORD)})


def history_download(request):
    """下载对应历史信息"""
    request_query = RequestQueryHandler(request)
    username, fullname, warename, action = (request_query.username, request_query.fullname, 
                                            request_query.warename, request_query.action)
    start_time, end_time = request_query.start_time, request_query.end_time
    users = User.objects.filter(username__icontains=username, full_name__icontains=fullname)
    query_string = dict(user_id__in=[uid[0] for uid in users.values_list("id")], 
                        create_date__gte=start_time, create_date__lte=end_time)
    if warename:
        query_string["affect_ware"] = warename
    if action:
        query_string["action"] = action
    histories = History.objects.filter(**query_string)
    filename = "用户历史 - 账户名_%s, 姓名_%s, 对象_%s, 动作_%s, 时间区间(%s, %s).xlsx" \
               % (username, fullname, warename, action, start_time, end_time) \
                 if any((username, fullname, warename, action, start_time, end_time)) else "用户历史.xlsx"
    file_wb = Workbook()
    file_sheet = file_wb.get_sheet_by_name(file_wb.sheetnames[0])
    file_sheet.title = "用户历史"
    # TODO: 这里下载
    file_sheet.append(["历史时间", "账户", "姓名", "动作", "影响"])
    for info in histories.order_by("-create_date"):
        the_user = User.objects.get(id=info.user_id)
        file_sheet.append([datetime.datetime.strftime(info.create_date, "%Y-%m-%d %H:%M:%S"),
                           the_user.username, the_user.full_name, dict(History.ACTION_RECORD).get(info.action, "error"),
                           "{the_model_cn} {the_object_cn}".format(
                               the_model_cn=dict(History.WARE_RECORD).get(info.affect_ware, "error"), 
                               the_object_cn=eval("%s.objects.filter(id=%s).first().__str__()"%(info.affect_ware, info.affect_object_id)))
                           ])
    response = HttpResponse(save_virtual_workbook(file_wb))
    response["Content-Type"] = "application/vnd.ms-excel"
    response["Content-Disposition"] = "attachment;filename=\"%s\"" % filename
    return response
