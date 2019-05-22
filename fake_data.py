import os
import random

import django
from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'worker_warehouse.settings')
django.setup()

from warehouse import models

faker_en = Faker(locale="en_US")
faker_cn = Faker(locale="zh_CN")


def choice_faker(rate_zh=0.6, rate_remark=0.7):
    fakers = list()
    flag1, flag2 = random.randrange(1, 10), random.randrange(1, 10)
    if flag1 > rate_zh*10:
        faker = faker_en
    else:
        faker = faker_cn
    fakers.append(faker)
    if flag2 > rate_remark*10:
        fakers.append(True)
    else: 
        fakers.append(False)
    return fakers


def create_data_supplier(count=50):
    ready = models.Supplier.objects.count()
    print("数据库Supplier中已有%s 个数据, 期望达到%s, 将会生成%s" % (ready, count, count-ready if ready<count else 0))
    if  ready < count:
        increase_num = count - ready
        while increase_num>0:
            faker, create_remark = choice_faker()
            new_data = models.Supplier(supplier_id=faker.ssn(), supplier_name=faker.company())
            if create_remark:
                new_data.remark = faker.text()
            new_data.save()
            increase_num -= 1


def create_data_classification(count=30):
    ready = models.Classification.objects.count()
    print("数据库Classification中已有%s 个数据, 期望达到%s, 将会生成%s" % (ready, count, count-ready if ready<count else 0))
    if ready < count:
        increase_num = count - ready
        while increase_num>0:
            faker, create_remark = choice_faker()
            new_data = models.Classification(class_name=faker.name())
            if create_remark:
                new_data.remark = faker.text()
            new_data.save()
            increase_num -= 1


if __name__ == "__main__":

    create_data_classification()
