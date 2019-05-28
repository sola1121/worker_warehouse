from django.urls import path, re_path

from . import views

app_name = "api"

urlpatterns = [
    path("history/", views.api_current_user_history, name="current_user_history"),
]
