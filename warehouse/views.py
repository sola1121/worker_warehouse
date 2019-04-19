from django.shortcuts import render

# Create your views here.

def supplier(request):
    return render(request, "app_warehouse/supplier.html", {"active_navbar": "supplier"})