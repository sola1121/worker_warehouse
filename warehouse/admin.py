from django.contrib import admin

from .models import Classification, Supplier, Warehouse, InWarehouse, OutWareHouse, Sale, History

# Register your models here.

@admin.register(Classification)
class ClassificationModelAdmin(admin.ModelAdmin):
    pass


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