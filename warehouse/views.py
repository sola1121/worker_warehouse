from django.shortcuts import render, redirect
from django.core.paginator import Paginator

from warehouse import models

# Create your views here.

PER_PAGE = 10

def supplier(request, page=1):
    supplier_id = request.GET.get("supplierId", None)
    supplier_name = request.GET.get("supplierName", None)
    print("============", supplier_id, supplier_name)
    suppliers = models.Supplier.objects.filter(is_deleted=False)
    if supplier_id:
        suppliers.filter(supplier_id__icontains=supplier_id)
    if supplier_name:
        suppliers.filter(supplier_name__icontains=supplier_name)
    paginator = Paginator(suppliers, PER_PAGE)
    if int(page) not in list(paginator.page_range):
        return redirect("/warehouse/supplier/")
    pagetor = paginator.get_page(page)
    return render(request, 
            "app_warehouse/supplier.html", 
            {"active_navbar": "supplier", 
             "pagetor": pagetor, 
             "supplier_id": supplier_id, 
             "supplier_name": supplier_name}
        )


def supplier_modify(request):
    pass


def supplier_delete(request):
    pass