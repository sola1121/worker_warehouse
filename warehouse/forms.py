from django.forms import ModelForm, TextInput, Textarea

from . import models


class SupplierForm(ModelForm):
    class Meta:
        model = models.Supplier
        fields = ["supplier_id", "supplier_name", "remark"]
        labels = {
            "supplier_id": "供应商编号",
            "supplier_name": "供应商名称",
            "remark": "备注"
            }
        widgets = {
            "supplier_id": TextInput(attrs={"id": "backend-supplierId", "class": "form-control",}),
            "supplier_name": TextInput(attrs={"id": "backend-supplierName", "class": "form-control"}),
            "remark": Textarea(attrs={"id": "backend-remark", "class": "form-control"}),
            }


