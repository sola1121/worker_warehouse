from django.urls import path

from . import views

app_name = "warehouse"

urlpatterns = [
    path("supplier", views.supplier, name="supplier_home"),
]