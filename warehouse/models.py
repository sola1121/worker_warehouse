from django.db import models

from account.models import User

# Create your models here.

class History(models.Model):
    """人员操作记录"""
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey("User", related_name="history", on_delete=models.SET("被删除"))
    action = models.CharField(verbose_name="用户活动", max_length=128)
    create_data = models.DateTimeField(verbose_name="活动发生时间", auto_now_add=True)

    def __str__(self):
        return "{}, {}, {}".format(self.create_data, str(User.objects.get(id=self.user_id).username), self.action)

    class Meta:
        db_name = "w_history"
        verbose_name = "用户操作记录"
        verbose_name_plural = "用户操作记录"


# class Units(models.Model):
#     """计件单位"""
#     id = models.AutoField(primary_key=True)


class Classification(models.Model):
    """物品分类"""
    id = models.AutoField(primary_key=True)
    class_name = models.CharField(verbose_name="物品种类", max_length=32, unique=True, null=False, db_index=True)
    remark = models.TextField(verbose_name="备注")

    def __str__(self):
        return self.class_name

    class Meta:
        db_table = "w_classification"
        verbose_name = "分类"
        verbose_name_plural = "分类"


class Supplier(models.Model):
    """供应商"""
    id = models.AutoField(primary_key=True)
    supplier_id = models.CharField(verbose_name="供应商编号", max_length=32, unique=True, null=False, db_index=True)
    supplier_name = models.CharField(verbose_name="供应商名称", max_length=64)
    remark = models.TextField(verbose_name="备注")

    def __str__(self):
        return "{}, {}".format(self.supplier_id, self.supplier_name)

    class Meta:
        db_table = "w_supplier"
        verbose_name = "供应商"
        verbose_name_plural = "供应商"


class Warehouse(models.Model):
    """货物存储库"""
    id = models.AutoField(primary_key=True)
    good_id = models.CharField(verbose_name="储物编号", max_length=32, unique=True, null=False, db_index=True)
    good_name = models.CharField(verbose_name="储物名称", max_length=64)
    # 分类外键
    classification = models.ForeignKey("Classification", null=True, related_name="warehouse", on_delete=models.SET_NULL)
    spec = models.CharField(verbose_name="规格/型号", max_length=32, default="未定义")
    amount = models.IntegerField(verbose_name="数量", default=0)
    unit = models.CharField(verbose_name="计件单位", max_length=32, default="未定义")
    price = models.FloatField(verbose_name="总金额", default=0)
    update_date = models.DateTimeField(verbose_name="更新时间", auto_now=True)
    remark = models.TextField(verbose_name="备注")
    # 供应商外键
    supplier = models.ForeignKey("Supplier", related_name="warehouse", on_delete=models.SET("数据删除"))

    def __str__(self):
        return "{}, {}".format(self.good_id, self.good_name)

    class Meta:
        db_table = "w_warehouse"
        verbose_name = "储物库"
        verbose_name_plural = "储物库"


class InWarehouse(models.Model):
    """货物入库记录"""
    id = models.AutoField(primary_key=True)
    good_id = models.CharField(verbose_name="储物编号", max_length=32, unique=True, null=False, db_index=True)
    good_name = models.CharField(verbose_name="储物名称", max_length=64)
    # 分类外键
    classification = models.ForeignKey("Classification", null=True, related_name="inWarehouse", on_delete=models.SET_NULL)
    spec = models.CharField(verbose_name="规格/型号", max_length=32, default="未定义")
    in_amount = models.IntegerField(verbose_name="数量", default=0)
    unit = models.CharField(verbose_name="计件单位", max_length=32, default="未定义")
    in_price = models.FloatField(verbose_name="总金额", default=0)
    create_date = models.DateTimeField(verbose_name="生成时间", auto_now_add=True)
    is_finished = models.BooleanField(verbose_name="是否完成", default=False)
    remark = models.TextField(verbose_name="备注")
    # 供应商外键
    supplier = models.ForeignKey("Supplier", related_name="inWarehouse", on_delete=models.SET("数据删除"))

    def __str__(self):
        return "{}, {}".format(self.good_id, self.good_name)

    class Meta:
        db_table = "w_in_warehouse"
        verbose_name = "入库单"
        verbose_name_plural = "入库单"


class OutWareHouse(models.Model):
    """货物出库记录"""
    id = models.AutoField(primary_key=True)
    good_id = models.CharField(verbose_name="储物编号", max_length=32, unique=True, null=False, db_index=True)
    good_name = models.CharField(verbose_name="储物名称", max_length=64)
    # 分类外键
    classification = models.ForeignKey("Classification", null=True, related_name="outWarehouse", on_delete=models.SET_NULL)
    spec = models.CharField(verbose_name="规格/型号", max_length=32, default="未定义")
    out_amount = models.IntegerField(verbose_name="数量", default=0)
    unit = models.CharField(verbose_name="计件单位", max_length=32, default="未定义")
    out_price = models.FloatField(verbose_name="总金额", default=0)
    create_date = models.DateTimeField(verbose_name="生成时间", auto_now_add=True)
    is_finished = models.BooleanField(verbose_name="是否完成", default=False)
    remark = models.TextField(verbose_name="备注")
    # 供应商外键
    supplier = models.ForeignKey("Supplier", related_name="outWarehouse", on_delete=models.SET("数据删除"))
    
    def __str__(self):
        return "{}, {}".format(self.good_id, self.good_name)

    class Meta:
        db_table = "w_out_warehouse"
        verbose_name = "出库单"
        verbose_name_plural = "出库单"
    

class Sale(models.Model):
    """销售记录"""
    id = models.AutoField(primary_key=True)
    good_id = models.CharField(verbose_name="商品编号", max_length=32, unique=True, null=False, db_index=True)
    good_name = models.CharField(verbose_name="商品名称", max_length=64)
    # 分类外键
    classification = models.ForeignKey("Classification", null=True, related_name="sale", on_delete=models.SET_NULL)
    spec = models.CharField(verbose_name="规格/型号", max_length=32, default="未定义")
    out_amount = models.IntegerField(verbose_name="数量", default=0)
    unit = models.CharField(verbose_name="计件单位", max_length=32, default="未定义")
    out_price = models.FloatField(verbose_name="销售金额", default=0)
    create_date = models.DateTimeField(verbose_name="生成时间", auto_now_add=True)
    is_finished = models.BooleanField(verbose_name="是否完成", default=False)
    remark = models.TextField(verbose_name="备注")
    # 供应商外键
    supplier = models.ForeignKey("Supplier", related_name="sale", on_delete=models.SET("数据删除"))
    # 出库单外键
    good_from = models.ForeignKey("OutWarehouse", null=True, related_name="sale", on_delete=models.SET_NULL)

    def __str__(self):
        return "{}, {}".format(self.good_id, self.good_name)

    class Meta:
        db_table = "w_sale"
        verbose_name = "销售单"
        verbose_name_plural = "销售单"