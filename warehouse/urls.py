from django.urls import path, re_path

from . import views, views_ware

app_name = "warehouse"

urlpatterns = [
    # 供应商管理
    path("supplier/", views.supplier, name="supplier_home"),
    re_path(r"supplier/(?P<page>\d.*?)/", views.supplier),
    path("supplier/modify/", views.supplier_modify, name="supplier_modify"),
    path("supplier/delete/", views.supplier_delete, name="supplier_delete"),
    path("supplier/download/", views.supplier_download, name="supplier_download"),

    # 物品分类管理
    path("classification/", views.classification, name="classification_home"),
    re_path(r"classification/(?P<page>\d.*?)/", views.classification),
    path("classification/modify/", views.classification_modify, name="classification_modify"),
    path("classification/delete/", views.classification_delete, name="classification_delete"),
    path("classification/download/", views.classification_download, name="classification_download"),

    # 入库单管理

    # 出库单管理

    # 在库管理
    path("warehouse/", views_ware.warehouse, name="warehouse_home"),
    re_path(r"warehouse/(?P<page>\d.*?)/", views_ware.warehouse),
    path("warehouse/modify/", views_ware.warehouse_modify, name="warehouse_modify"),
    path("warehouse/delete/", views_ware.warehouse_delete, name="warehouse_delete"),
    path("warehouse/download/", views_ware.warehouse_download, name="warehouse_download"),
    # 销售单管理
]