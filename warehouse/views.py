from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.core.paginator import Paginator

from warehouse import models, forms

# Create your views here.

OK = "OK"
PER_PAGE = 10

### 供应商相关 ###

def supplier(request, page=1):
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
    form = forms.SupplierForm()
    # TODO: 通过GET方式传递supplier_id, 来对相应的表单进行编辑
    if request.method == "POST":
        data = request.POST
        print(data)
        return JsonResponse({"back_msg": OK})
    return render(request, 
                  "app_warehouse/supplier_change.html", 
                  {"head_title": "添加供应商",
                   "active_navbar": "supplier",
                   "form": form})


def supplier_delete(request):
    supplier_id = request.POST.get("supplierId", '')
    try:
        supplier = models.Supplier.objects.get(supplier_id=supplier_id)
    except:
        return JsonResponse({"back_msg": "数据库出错, 未能正确删除内容."})
    supplier.is_deleted = True
    supplier.save()
    return JsonResponse({"back_msg": OK})


def supplier_download(request):
    pass