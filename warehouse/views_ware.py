import datetime
import logging

import pytz
from openpyxl import Workbook
from openpyxl.writer.excel import save_virtual_workbook
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, FileResponse, Http404
from django.core.paginator import Paginator

from account.models import History
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
        # 针对入库单的
        self.person_liable = request.GET.get("personLiable", '')
        self.is_finished = request.GET.get("isFinished", '')
    
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


### 在库相关 ###

@login_required(login_url="/")
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
    paginator = Paginator(warehouses.order_by("-update_date"), PER_PAGE)
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


@login_required(login_url="/")
def warehouse_modify(request):
    """在库货物添加和修改"""
    good_id = request.GET.get("goodId", '')
    form = forms.WarehouseForm()
    if good_id:
        warehouse = get_object_or_404(models.Warehouse, good_id=good_id)
        form = forms.WarehouseForm(instance=warehouse)

    if request.method == "POST":
        action = History.CREATE
        origin_good_id = request.POST.get("origin_good_id", '')
        if origin_good_id:
            try:
                action = History.MODIFY
                change_good_id = request.POST.get("good_id")
                if origin_good_id != change_good_id:
                    is_exist_warehouse = models.Warehouse.objects.filter(good_id=change_good_id).exists()   # 保证不和数据库中已有唯一冲突
                    if is_exist_warehouse:
                        raise AssertionError("warehouse objetcts with %s has aready existed."%change_good_id)
                origin_warehouse = models.Warehouse.objects.get(good_id=origin_good_id)
            except AssertionError:
                return JsonResponse({"back_msg": "%s 储物编号已经存在."%change_good_id})
            except Exception:
                return JsonResponse({"back_msg": "源数据取出失败."})
        else:
            return JsonResponse({"back_msg": "未获取到储物编号."})   # 确保必须要有原始的储物数据
        pk_id = origin_warehouse.id   # 保留更改对象的pk, 以免关联的表出错
        origin_warehouse.delete()
        form = forms.WarehouseForm(request.POST)
        if form.is_valid():
            new_warehouse = form.save(commit=False)
            new_warehouse.id = pk_id
            new_warehouse.amount = int(new_warehouse.amount) if int(new_warehouse.amount)>=0 else 0
            new_warehouse.save()
            # NOTE: 向history中存入记录
            new_history = History.set_record(cur_user=request.user, model=new_warehouse, act=action)
            new_history.save()
            return JsonResponse({"back_msg": OK})
        else:
            origin_warehouse.save()   # 恢复原先删除
            full_msg = str()
            for value in form.errors.values():
                for msg in value: 
                    full_msg += msg + "\n" 
            return JsonResponse({"back_msg": full_msg})

    return render(request, 
                  "app_warehouse/warehouse_change.html", 
                  {"head_title": "编辑在库货物",
                   "active_navbar": "warehouse",
                   "form": form})


@login_required(login_url="/")
def warehouse_delete(request):
    """储物删除"""
    good_id = request.POST.get("goodId", '')
    try:
        warehouse = models.Warehouse.objects.get(good_id=good_id)
    except:
        return JsonResponse({"back_msg": "数据库出错, 未能正确删除内容."})
    warehouse.is_deleted = True
    warehouse.good_id = str(warehouse.supplier_id) + "(DELETED %s)"%datetime.datetime.now(TZ).strftime("%Y-%m-%d %H:%M:%S %f")   # 避免删除后对添加或修改会有唯一性冲突
    warehouse.save()
    # NOTE: history中存入记录
    new_history = History.set_record(cur_user=request.user, model=warehouse, act=History.DELETE)
    new_history.save()
    return JsonResponse({"back_msg": OK})


@login_required(login_url="/")
def warehouse_download(request):
    """下载查询结果"""
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
    filename = "储物库 - 编号_%s, 名称_%s, 分类_%s, 供应编号_%s, 供应商名_%s, 时间区间(%s, %s).xlsx" \
               % (good_id, good_name, class_name, supplier_id, supplier_name, start_time, end_time) \
                 if any((good_id, good_name, class_name, supplier_id, supplier_name, start_time, end_time)) else "储物库.xlsx"
    file_wb = Workbook()
    file_sheet = file_wb.get_sheet_by_name(file_wb.sheetnames[0])
    file_sheet.title = "储物库"
    file_sheet.append(["储物编号", "储物名称", "储物分类", "供应商编号", "供应商名称", "规格/型号", "计件单位", "储物数量", "总金额", "最近更新", "备注"])
    for info in warehouses.order_by("-update_date"):
        file_sheet.append([info.good_id, info.good_name, info.classification.class_name, info.supplier.supplier_id, info.supplier.supplier_name, 
                           info.spec, info.unit, info.amount, info.price, datetime.datetime.strftime(info.update_date, "%Y-%m-%d %H:%M:%S"),
                           str(info.remark).replace('\n', '').replace('\r', '') if info.remark else ''])
    response = HttpResponse(save_virtual_workbook(file_wb))
    response["Content-Type"] = "application/vnd.ms-excel"
    response["Content-Disposition"] = "attachment;filename=\"%s\"" % filename
    return response


### 入库相关 ###

@login_required(login_url='/')
def in_warehouse(request, page=1):
    return render(request, 
                  "app_warehouse/in_warehouse.html",
                  {"active_navbar": "inwarehouse",
                  })


@login_required(login_url='/')
def in_warehouse_modify(request):
    """入库单添加和修改"""
    the_id = request.GET.get("id", '')
    form = forms.InWarehouseForm()
    if the_id:
        inwarehouse = get_object_or_404(models.InWarehouse, id=the_id)
        form = forms.InWarehouseForm(instance=inwarehouse)

    if request.method == "POST":
        action = History.CREATE
        origin_id = request.POST.get("origin_id", '')
        if origin_id:
            try:
                action = History.MODIFY
                origin_inwarehouse = models.InWarehouse.objects.get(id=origin_id)
                if origin_inwarehouse.is_finished:
                    raise AssertionError("order have finished, %s" %origin_id)   # 已经完成的订单不能修改
            except AssertionError:
                return JsonResponse({"back_msg": "%s 入库单已经存在." %origin_inwarehouse})
            except Exception:
                return JsonResponse({"back_msg": "源数据取出失败."})
        pk_id = origin_inwarehouse.id   # 保留更改对象的pk, 以免关联的表出错
        origin_inwarehouse.delete()
        form = forms.WarehouseForm(request.POST)
        if form.is_valid():
            new_inwarehouse = form.save(commit=False)
            new_inwarehouse.id = pk_id
            new_inwarehouse.in_amount = int(new_inwarehouse.in_amount) if int(new_inwarehouse.in_amount)>=0 else 0
            new_inwarehouse.save()
            # NOTE: 向history中存入记录
            new_history = History.set_record(cur_user=request.user, model=new_inwarehouse, act=action)
            new_history.save()
            return JsonResponse({"back_msg": OK})
        else:
            origin_inwarehouse.save()   # 恢复原先删除
            full_msg = str()
            for value in form.errors.values():
                for msg in value: 
                    full_msg += msg + "\n" 
            return JsonResponse({"back_msg": full_msg})

    return render(request, 
                  "app_warehouse/in_warehouse_change.html", 
                  {"head_title": "编辑入库单",
                   "active_navbar": "inwarehouse",
                   "form": form})


def in_warehouse_delete(request):
    pass


def in_warehouse_check(request):
    pass


def in_warehouse_download(request):
    pass


### 出库相关 ###