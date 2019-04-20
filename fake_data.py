import os
import random

import django
from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'worker_warehouse.settings')
django.setup()

from warehouse import models

faker_en = Faker(locale="en_US")
faker_cn = Faker(locale="zh_CN")

count = 50
ready = models.Supplier.objects.count()
print("数据库Supplier中已有%s 个数据, 期望达到%s, 将会生成%s" % (ready, count, count-ready if ready<count else 0))
if  ready < count:
    increase_num = count - ready
    while increase_num>0:
        flag1, flag2 = random.randrange(1, 10), random.randrange(1, 100)
        if flag1 > 7:
            faker = faker_en
        else:
            faker = faker_cn
        new_supplier = models.Supplier(supplier_id=faker.ssn(), supplier_name=faker.company())
        if flag2 > 70:
            new_supplier.remark = faker.text()
        new_supplier.save()
        increase_num -= 1
