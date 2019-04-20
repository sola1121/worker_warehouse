from django.urls import path, re_path

from . import views

app_name = "warehouse"

urlpatterns = [
    re_path(r"supplier/(?P<page>\d.*?)/", views.supplier),
    path("supplier/", views.supplier, name="supplier_home"),
]