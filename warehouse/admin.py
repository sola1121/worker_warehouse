from django.contrib import admin

# Register your models here.

from django.contrib import admin

from .models import Supplier, Warehouse, InWarehouse, OutWareHouse, Sale, History

# Register your models here.

admin.site.site_title = "数据库后台管理"
admin.site.site_header = "数据库管理界面"


@admin.register(Supplier)
class SupplierModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Warehouse)
class WarehouseModelAdmin(admin.ModelAdmin):
    pass


@admin.register(InWarehouse)
class InWarehouseModelAdmin(admin.ModelAdmin):
    pass


@admin.register(OutWareHouse)
class OutWareHouseModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Sale)
class SaleModelAdmin(admin.ModelAdmin):
    pass


@admin.register(History)
class HistoryModelAdmin(admin.ModelAdmin):
    pass