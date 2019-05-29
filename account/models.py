import datetime

from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    """自定义的用户表, 通过绝对对象继承"""
    full_name = models.CharField(verbose_name="姓名", max_length=32)
    phone = models.CharField(verbose_name="手机号码", max_length=16)

    def __str__(self):
        return "%s - %s" % (self.username, self.full_name)

    class Meta:
        db_table = "w_user"
        verbose_name = "用户"
        verbose_name_plural = "用户"


class History(models.Model):
    """人员操作记录"""
    WARE_RECORD =[
        ("Supplier", "供应商"),
        ("Classification", "储物分类"),
        ("InWarehouse", "入库记录单"),
        ("OutWarehouse", "出库记录单"),
        ("Warehouse", "储物库"),
        ("Sale", "销售单"),
    ]

    CREATE, MODIFY, DELETE = "CREATE", "MODIFY", "DELETE"
    ACTION_RECORD = [
        (CREATE, "创建"),
        (MODIFY, "修改"),
        (DELETE, "删除"),
    ]

    id = models.AutoField(primary_key=True)
    user_id = models.IntegerField(verbose_name="操作用户的主键")
    affect_ware = models.CharField(verbose_name="受影响的表", max_length=32, choices=WARE_RECORD)
    affect_object_id = models.IntegerField(verbose_name="受影响表的对象主键")
    action = models.CharField(verbose_name="用户活动描述", max_length=16, choices=ACTION_RECORD)
    create_date = models.DateTimeField(verbose_name="活动发生时间", auto_now_add=True)

    def __str__(self):
        return "{} - {} - {}".format(self.create_date, str(User.objects.get(id=self.user_id).username), self.action)

    @classmethod
    def set_record(cls, cur_user, model, act):
        """cur_user当前的用户对象, model受影响的模型, act记录动作消息"""
        if not issubclass(model.__class__, models.Model):
            raise ValueError("Unknown model object %s, it's must be a subclass of models.Model." % type(model))
        new_cls = cls(user_id=cur_user.id, 
                      affect_ware=model.get_model_name(), 
                      affect_object_id=model.id, 
                      action=act)
        return new_cls

    def get_record(self):
        import warehouse.models as ware_models
        cur_user = User.objects.get(id=self.user_id)
        return "{the_time} {the_account}({the_fullname}) {the_action_cn} {the_model_name_cn} {the_model_object}".format(
                the_time=datetime.datetime.strftime(self.create_date, "%Y-%m-%d %H:%M:%S"),
                the_account=cur_user.username,
                the_fullname=cur_user.full_name,
                the_model_name_cn=dict(self.WARE_RECORD)[self.affect_ware],
                the_model_object=eval("ware_models.%s.objects.filter(id=%s).first().__str__()"%(self.affect_ware, self.affect_object_id)),
                the_action_cn=dict(self.ACTION_RECORD)[self.action]
            )

    class Meta:
        db_table = "w_history"
        verbose_name = "用户操作记录"
        verbose_name_plural = "用户操作记录"
        ordering = ["-id", "-create_date"]
