from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
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
    paginator = Paginator(suppliers, PER_PAGE)
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
    """供应商添加与修改"""
    supplier_id = request.GET.get("supplierId", '')
    form = forms.SupplierForm()
    if supplier_id:
        supplier = get_object_or_404(models.Supplier, supplier_id=supplier_id)
        print(supplier)
        form = forms.SupplierForm(instance=supplier)
    if request.method == "POST":
        form = forms.SupplierForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({"back_msg": OK})
        else:
            print(form.errors)
            return JsonResponse({"back_msg": "保存失败"})
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
    pass