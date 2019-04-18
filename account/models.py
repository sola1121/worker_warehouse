from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class User(AbstractUser):
    full_name = models.CharField(verbose_name="姓名", max_length=32)
    phone = models.CharField(verbose_name="手机号码", max_length=16)

    def __str__(self):
        return "%s - %s" % (self.username, self.full_name)

    class Meta:
        db_table = "w_user"
        verbose_name = "用户"
        verbose_name_plural = "用户"
    