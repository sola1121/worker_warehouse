from django.contrib import admin

from .models import Classification, Supplier, Warehouse, InWarehouse, OutWareHouse, Sale

# Register your models here.

@admin.register(Classification)
class ClassificationModelAdmin(admin.ModelAdmin):
    pass


@admin.register(Supplier)
class SupplierModelAdmin(admin.ModelAdmin):
    search_fields = ("suplier_id", "supplier_name")
    sortable_by = ("id",)
    list_display = ("id", "supplier_id", "supplier_name", "is_deleted", "short_remark")
    list_display_links = ("id", "supplier_id", "supplier_name")


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
