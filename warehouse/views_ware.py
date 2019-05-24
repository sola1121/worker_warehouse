import datetime

from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse, FileResponse, Http404
from django.core.paginator import Paginator

from warehouse import models, forms

# Create your views here.

OK = "OK"
PER_PAGE = 10

class RequestQueryHandler:
    def __init__(self, request):
        self.supplier_id = request.GET.get("supplierId", '')
        self.supplier_name = request.GET.get("supplierName", '')
        self.good_id = request.GET.get("goodId", '')
        self.good_name = request.GET.get("goodName", '')
        self.class_name = request.GET.get("className", '')
        self.time_deal(request)
    
    def time_deal(self, request):
        start_time = request.GET.get("startTime", '')
        end_time = request.GET.get("endTime", '')
        self.origin_start_time, self.origin_end_time = start_time, end_time
        try:
            if start_time:
                self.start_time = datetime.datetime.strptime(start_time, "%Y-%m-%d")
            else:
                self.start_time = datetime.datetime(1970, 1, 1, 0, 0)
            if end_time:
                self.end_time = datetime.datetime.strptime(end_time, "%Y-%m-%d")
            else:
                self.end_time = datetime.datetime.now()
            if start_time and end_time:
                if self.start_time > self.end_time:
                    self.start_time, self.end_time = self.end_time, self.start_time
        except:
            raise Http404

### 入库相关 ###

### 出库相关 ###

### 在库相关 ###

def warehouse(request, page=1):
    """在库货物显示与查询"""
    request_query = RequestQueryHandler(request)
    supplier_id, supplier_name = request_query.supplier_id, request_query.supplier_name
    good_id, good_name = request_query.good_id, request_query.good_name
    class_name = request_query.class_name
    start_time, end_time = request_query.start_time, request_query.end_time
    warehouses = models.Warehouse.objects.filter(is_deleted=False,
                                                 supplier__supplier_id__icontains=supplier_id,
                                                 supplier__supplier_name__icontains=supplier_name,
                                                 classification__class_name__icontains=class_name,
                                                 good_id__icontains=good_id,
                                                 good_name__icontains=good_name,
                                                 update_date__gte=start_time,
                                                 update_date__lte=end_time)
    # warehouses = models.Warehouse.objects.all()
    paginator = Paginator(warehouses.order_by("update_date"), PER_PAGE)
    if int(page) not in list(paginator.page_range):
        return redirect("/warehouse/warehouse/")
    pagetor = paginator.get_page(page)
    return render(request, 
                  "app_warehouse/warehouse.html",
                  {"active_navbar": "warehouse",
                   "pagetor": pagetor,
                   "supplier_id": supplier_id,
                   "supplier_name": supplier_name,
                   "good_id": good_id,
                   "good_name": good_name,
                   "class_name": class_name,
                   "start_time": request_query.origin_start_time,
                   "end_time": request_query.origin_end_time})


def warehouse_modify(request):
    pass


def warehouse_delete(request):
    pass


def warehouse_download(request):
    pass