from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse, FileResponse
from django.core.paginator import Paginator

from warehouse import models, forms

# Create your views here.

OK = "OK"
PER_PAGE = 10

### 供应商相关 ###

def supplier(request, page=1):
    """供应商页面显示与查询"""
    supplier_id = request.GET.get("supplierId", '')
    supplier_name = request.GET.get("supplierName", '')
    suppliers = models.Supplier.objects.filter(is_deleted=False, 
                                               supplier_id__icontains=supplier_id, 
                                               supplier_name__icontains=supplier_name)
    paginator = Paginator(suppliers.order_by("-id"), PER_PAGE)
    if int(page) not in list(paginator.page_range):
        return redirect("/warehouse/supplier/")
    pagetor = paginator.get_page(page)
    return render(request, 
                  "app_warehouse/supplier.html", 
                  {"active_navbar": "supplier", 
                   "pagetor": pagetor, 
                   "supplier_id": supplier_id, 
                   "supplier_name": supplier_name})


def supplier_modify(request):
    """供应商添加和修改"""
    supplier_id = request.GET.get("supplierId", '')
    form = forms.SupplierForm()
    if supplier_id:
        supplier = get_object_or_404(models.Supplier, supplier_id=supplier_id)
        form = forms.SupplierForm(instance=supplier)

    if request.method == "POST":
        origin_supplier_id = request.POST.get("origin_supplier_id", '')
        if origin_supplier_id:
            try:
                origin_supplier = models.Supplier.objects.get(supplier_id=origin_supplier_id)
                origin_supplier.delete()
            except:
                return JsonResponse({"back_msg": "源数据取出失败."})
        form = forms.SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            # TODO: 应该向history中存入记录
            return JsonResponse({"back_msg": OK})
        else:
            return JsonResponse({"back_msg": form.errors.get_json_data(escape_html=True)})

    return render(request, 
                  "app_warehouse/supplier_change.html", 
                  {"head_title": "编辑供应商",
                   "active_navbar": "supplier",
                   "form": form})


def supplier_delete(request):
    """供应商删除"""
    supplier_id = request.POST.get("supplierId", '')
    try:
        supplier = models.Supplier.objects.get(supplier_id=supplier_id)
    except:
        return JsonResponse({"back_msg": "数据库出错, 未能正确删除内容."})
    supplier.is_deleted = True
    supplier.save()
    # TODO: 应该向history中存入记录
    return JsonResponse({"back_msg": OK})


def supplier_download(request):
    """下载查询结果"""
    supplier_id = request.GET.get("supplierId", '')
    supplier_name = request.GET.get("supplierName", '')
    suppliers = models.Supplier.objects.filter(is_deleted=False, 
                                               supplier_id__icontains=supplier_id, 
                                               supplier_name__icontains=supplier_name)
    filename = "供应商 - 搜索编号_%s, 搜索名称_%s.xlsx" % (supplier_id, supplier_name) if any((supplier_id, supplier_name)) else "供应商.xlsx"
    file_wb = Workbook()
    file_sheet = file_wb.get_sheet_by_name(file_wb.sheetnames[0])
    file_sheet.title = "供应商"
    file_sheet.append(["供应商编号", "供应商名称", "备注"])
    for info in suppliers.values():
        file_sheet.append([info["supplier_id"], info["supplier_name"], info["remark"].replace('\n', '').replace('\r', '')])
    response = HttpResponse(save_virtual_workbook(file_wb))
    response["Content-Type"] = "application/vnd.ms-excel"
    response["Content-Disposition"] = "attachment;filename=\"%s\"" % filename
    return response


### 物品种类相关 ###

def classification(request, page=1):
    """物品分类的查询与显示"""
    class_name = request.GET.get("className", '')
    classifications = models.Classification.objects.filter(is_deleted=False, 
                                                           class_name__icontains=class_name)
    paginator = Paginator(classifications.order_by("-id"), PER_PAGE)
    if int(page) not in list(paginator.page_range):
        return redirect("/warehouse/classification/")
    pagetor = paginator.get_page(page)
    return render(request, 
                  "app_warehouse/classification.html", 
                  {"active_navbar": "classification", 
                   "pagetor": pagetor, 
                   "class_name": class_name})


def classification_modify(request):
    """添加和更改相应的物品分类"""
    class_name = request.GET.get("className", '')
    form = forms.ClassificationForm()
    if class_name:
        classification = get_object_or_404(models.Classification, class_name=class_name)
        form = forms.ClassificationForm(instance=classification)

    if request.method == "POST":
        origin_class_name = request.POST.get("origin_class_name", '')
        if origin_class_name:
            try:
                origin_classification = models.Classification.objects.get(class_name=origin_class_name)
                origin_classification.delete()
            except:
                return JsonResponse({"back_msg": "源数据取出失败."})
        form = forms.ClassificationForm(request.POST)
        if form.is_valid():
            form.save()
            # TODO: 应该向history中存入记录
            return JsonResponse({"back_msg": OK})
        else:
            return JsonResponse({"back_msg": form.errors.get_json_data(escape_html=True)})

    return render(request, 
                  "app_warehouse/classification_change.html", 
                  {"head_title": "编辑物品分类",
                   "active_navbar": "classification",
                   "form": form})


def classification_delete(request):
    """物品分类删除"""
    class_name = request.POST.get("className", '')
    try:
        classification = models.classification.objects.get(class_name=class_name)
    except:
        return JsonResponse({"back_msg": "数据库出错, 未能正确删除内容."})
    classification.is_deleted = True
    classification.save()
    # TODO: 应该向history中存入记录
    return JsonResponse({"back_msg": OK})


def classification_download(request):
    """下载物品分类"""
    class_name = request.GET.get("className", '')
    classifications = models.Classification.objects.filter(is_deleted=False, 
                                                           class_name__icontains=class_name)
    filename = "物品分类 - 搜索名称_%s.xlsx" % class_name if any((class_name,)) else "物品分类.xlsx"
    file_wb = Workbook()
    file_sheet = file_wb.get_sheet_by_name(file_wb.sheetnames[0])
    file_sheet.title = "物品分类"
    file_sheet.append(["物品分类名称", "备注"])
    for info in classifications.values():
        file_sheet.append([info["class_name"], info["remark"].replace('\n', '').replace('\r', '')])
    response = HttpResponse(save_virtual_workbook(file_wb))
    response["Content-Type"] = "application/vnd.ms-excel"
    response["Content-Disposition"] = "attachment;filename=\"%s\"" % filename
    return response


### 销售单管理 ###
