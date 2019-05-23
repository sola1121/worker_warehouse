from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse, FileResponse
from django.core.paginator import Paginator

from warehouse import models, forms

# Create your views here.

OK = "OK"
PER_PAGE = 10


### 入库相关 ###

### 出库相关 ###

### 在库相关 ###

def warehouse(request, page=1):
    """在库货物显示与查询"""
    return render(request, 
                  "app_warehouse/warehouse.html",
                  {"active_navbar": "warehouse",})


def warehouse_modify(request):
    pass


def warehouse_delete(request):
    pass


def warehouse_download(request):
    pass