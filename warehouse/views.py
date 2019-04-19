from django.shortcuts import render
from django.core.paginator import Paginator

from warehouse import models

# Create your views here.

PER_PAGE = 5

def supplier(request, page=10):
    print("接收页数", page)
    supplier_id = request.GET.get("supplier_id", None)
    supplier_name = request.GET.get("supplier_name", None)
    suppliers = models.Supplier.objects.all()
    if supplier_id:
        suppliers.filter(supplier_id__icontains=supplier_id)
    if supplier_name:
        suppliers.filter(supplier_name__icontains=supplier_name)
    paginator = Paginator(suppliers, PER_PAGE)
    pagetor = paginator.get_page(page)
    return render(request, "app_warehouse/supplier.html", {"active_navbar": "supplier", "pagetor": pagetor})
