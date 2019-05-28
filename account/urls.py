from django.urls import path, re_path

from . import views


app_name = "account"

urlpatterns = [
    # 用户登录, 登出, 修改密码
    path('', views.account_login, name="account_login"),
    path("logout", views.account_logout, name="account_logout"),
    path("account/change", views.account_change_password, name="account_change"),

    # 用户历史浏览
    path("history/", views.history, name="history_home"),
    re_path(r"history/(?P<page>\d.*?)/", views.history),
]