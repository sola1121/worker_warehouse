import datetime
import logging

import pytz
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook
from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse, HttpResponse, FileResponse, Http404
from django.core.paginator import Paginator

from warehouse import models, forms

# Create your views here.

OK = "OK"
TZ = pytz.timezone("Asia/Shanghai")
PER_PAGE = 10

class RequestQueryHandler:
    """处理GET请求参数"""
    def __init__(self, request):
        self.supplier_id = request.GET.get("supplierId", '')
        self.supplier_name = request.GET.get("supplierName", '')
        self.good_id = request.GET.get("goodId", '')
        self.good_name = request.GET.get("goodName", '')
        self.class_name = request.GET.get("className", '')
        self._time_deal(request)
    
    def _time_deal(self, request):
        start_time = request.GET.get("startTime", '')
        end_time = request.GET.get("endTime", '')
        self.origin_start_time, self.origin_end_time = start_time, end_time
        try:
            if start_time:
                trans_time = datetime.datetime.strptime(start_time, "%Y-%m-%d") - datetime.timedelta(days=1)
                self.start_time = datetime.datetime(trans_time.year, trans_time.month, trans_time.day, tzinfo=TZ)
            else:
                self.start_time = datetime.datetime(1970, 1, 1, 0, 0, tzinfo=TZ)
            if end_time:
                trans_time = datetime.datetime.strptime(end_time, "%Y-%m-%d") + datetime.timedelta(days=1)
                self.end_time = datetime.datetime(trans_time.year, trans_time.month, trans_time.day, tzinfo=TZ)
            else:
                self.end_time = datetime.datetime.now(TZ)
            if start_time and end_time:
                if self.start_time > self.end_time:
                    self.start_time, self.end_time = self.end_time, self.start_time
        except Exception as ex:
            logging.error(ex)
            return render(request, "exceptions/500.html", status=500)

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
    """在库货物添加和修改"""
    good_id = request.GET.get("goodId", '')
    form = forms.WarehouseForm()
    if good_id:
        warehouse = get_object_or_404(models.Warehouse, good_id=good_id)
        form = forms.WarehouseForm(instance=warehouse)

    if request.method == "POST":
        origin_good_id = request.POST.get("origin_good_id", '')
        if origin_good_id:
            try:
                change_good_id = request.POST.get("good_id")
                is_exist_warehouse = models.Warehouse.objects.filter(good_id=change_good_id).exists()
                if is_exist_warehouse:
                    raise AssertionError("warehouse objetcts with %s has aready existed."%change_good_id)
                origin_warehouse = models.Warehouse.objects.get(good_id=good_id)
                print(origin_warehouse)
                # origin_warehouse.delete()
            except AssertionError:
                return JsonResponse({"back_msg": "%s 储物编号已经存在."})
            except:
                return JsonResponse({"back_msg": "源数据取出失败."})
        else:
            return JsonResponse({"back_msg": "未获取到储物编号"})   # 确保必须要有原始的储物数据
        # TODO: 删除, 要看看select的widget的返回的value是啥
        print(request.POST.get("supplier"))
        print(request.POST.get("classification"))
        form = forms.WarehouseForm(request.POST)
        if form.is_valid():
            # form.save()
            print("这里需要验证一下\n", form)
            # TODO: 应该向history中存入记录
            return JsonResponse({"back_msg": OK})
        else:
            return JsonResponse({"back_msg": form.errors.get_json_data(escape_html=True)})

    return render(request, 
                  "app_warehouse/warehouse_change.html", 
                  {"head_title": "编辑在库货物",
                   "active_navbar": "warehouse",
                   "form": form})


def warehouse_delete(request):
    """储物删除"""
    supplier_id = request.POST.get("supplierId", '')
    try:
        supplier = models.Supplier.objects.get(supplier_id=supplier_id)
    except:
        return JsonResponse({"back_msg": "数据库出错, 未能正确删除内容."})
    supplier.is_deleted = True
    supplier.supplier_id = str(supplier.supplier_id) + "(DELETE%s)"%datetime.datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S %f")   # 避免删除后对添加或修改会有唯一性冲突
    supplier.save()
    # TODO: 应该向history中存入记录
    return JsonResponse({"back_msg": OK})


def warehouse_download(request):
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