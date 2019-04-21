from django.urls import path, re_path

from . import views

app_name = "warehouse"

urlpatterns = [
    path("supplier/", views.supplier, name="supplier_home"),
    re_path(r"supplier/(?P<page>\d.*?)/", views.supplier),
    path("supplier/modify/", views.supplier_modify, name="supplier_modify"),
    path("supplier/delete/", views.supplier_delete, name="supplier_delete"),
]