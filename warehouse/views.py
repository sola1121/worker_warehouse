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
        print(supplier)
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

# TODO: