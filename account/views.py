from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required

from .models import User

# Create your views here.


def account_login(request):
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
    logout(request)
    return render(request, "app_account/login.html")


@login_required(login_url="/")
def account_change_password(request):
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
