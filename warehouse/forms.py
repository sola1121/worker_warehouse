from django.forms import ModelForm, TextInput, Textarea, Select, NumberInput, CheckboxInput
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
            "supplier_id": TextInput(attrs={"id": "backend-supplierId", "class": "form-control", "required": True}),
            "supplier_name": TextInput(attrs={"id": "backend-supplierName", "class": "form-control", "required": True}),
            "remark": Textarea(attrs={"id": "backend-remark", "class": "form-control"}),
        }


class ClassificationForm(ModelForm):
    class Meta:
        model = models.Classification
        fields = ["class_name", "remark"]
        labels = {
            "class_name": "物品分类名",
            "remark": "备注"
        }
        widgets = {
            "class_name": TextInput(attrs={"id": "backend-className", "class": "form-control", "required": True}),
            "remark": Textarea(attrs={"id": "backend-remark", "class": "form-control"}),
        }


class InWarehouseForm(ModelForm):
    class Meta:
        model = models.InWarehouse
        fields = ["good_id", "good_name", "classification", "person_liable", "supplier", "spec", "in_amount", "unit", "in_price", "is_finished", "remark"]
        # 供应商外键
        labels = {
            "good_id": "入库货物在库编号",
            "good_name": "货物名称",
            "classification": "货物分类",
            "person_liable": "负责人",
            "supplier": "供应商",
            "spec": "规格/型号",
            "unit": "计件单位",
            "in_amount": "入库数量",
            "in_price": "入库货物金额",
            "is_finished": "是否已入库完毕",
            "remark": "备注" 
        }
        widgets = {
            "good_id": TextInput(attrs={"id": "backend-goodId", "class": "form-control", "required": True}),
            "good_name": TextInput(attrs={"id": "backend-goodName", "class": "form-control", "required": True}),
            "classification": Select(attrs={"id": "backend-classification", "class": "form-control"}),
            "person_liable": TextInput(attrs={"id": "backend-personLiable", "class": "form-control"}),
            "supplier": Select(attrs={"id": "backend-supplier", "class": "form-control"}),
            "spec": TextInput(attrs={"id": "backend-spec", "class": "form-control"}),
            "unit": TextInput(attrs={"id": "backend-unit", "class": "form-control"}),
            "in_amount": NumberInput(attrs={"id": "backend-inAmount", "class": "form-control", "step": "1", "min": 0}),
            "in_price": NumberInput(attrs={"id": "backend-inPrice", "class": "form-control", "step": "0.01", "min": 0}),
            "is_finished": CheckboxInput(attrs={"id": "backend-isFinished", "class": "form-control", "value": 0}),
            "remark": Textarea(attrs={"id": "backend-remark", "class": "form-control"}),
        }


class OutWarehouseForm(ModelForm):
    pass


class WarehouseForm(ModelForm):
    class Meta:
        model = models.Warehouse
        fields = ["good_id", "good_name", "classification", "supplier", "spec", "unit", "amount", "price", "remark"]
        labels = {
            "good_id": "储物编号",
            "good_name": "储物名称",
            "classification": "储物分类",
            "supplier": "供应商",
            "spec": "规格/型号",
            "unit": "计件单位",
            "amount": "数量",
            "price": "总金额",
            "remark": "备注" 
        }
        widgets = {
            "good_id": TextInput(attrs={"id": "backend-goodId", "class": "form-control", "required": True}),
            "good_name": TextInput(attrs={"id": "backend-goodName", "class": "form-control", "required": True}),
            "classification": Select(attrs={"id": "backend-classification", "class": "form-control"}),
            "supplier": Select(attrs={"id": "backend-supplier", "class": "form-control"}),
            "spec": TextInput(attrs={"id": "backend-spec", "class": "form-control"}),
            "unit": TextInput(attrs={"id": "backend-unit", "class": "form-control"}),
            "amount": NumberInput(attrs={"id": "backend-amount", "class": "form-control", "step": "1", "min": 0}),
            "price": NumberInput(attrs={"id": "backend-price", "class": "form-control", "step": "0.01", "min": 0}),
            "remark": Textarea(attrs={"id": "backend-remark", "class": "form-control"}),
        }