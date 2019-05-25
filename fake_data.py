import os
import random
import datetime

import django
from faker import Faker

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'worker_warehouse.settings')
django.setup()

from warehouse import models

faker_en = Faker(locale="en_US")
faker_cn = Faker(locale="zh_CN")

hit_describe = "数据库%s中已有%s 个数据, 期望达到%s, 将会生成%s"

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
    print(hit_describe % ("Supplier", ready, count, count-ready if ready<count else 0))
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
    print(hit_describe % ("Classification", ready, count, count-ready if ready<count else 0))
    if ready < count:
        increase_num = count - ready
        while increase_num>0:
            faker, create_remark = choice_faker()
            new_data = models.Classification(class_name=faker.name())
            if create_remark:
                new_data.remark = faker.text()
            new_data.save()
            increase_num -= 1


def create_data_InWarehouse(count=20):
    pass


def create_data_OutWarehouse(count=20):
    pass


def create_data_warehouse(count=40):
    ready = models.Warehouse.objects.count()
    print(hit_describe % ("Warehouse", ready, count, count-ready if ready<count else 0))
    if ready < count:
        increase_num = count - ready
        while increase_num>0:
            faker, create_remark = choice_faker()
            new_classification = [pk[0] for pk in models.Classification.objects.filter(is_deleted=False).values_list("id")]
            new_supplier = [pk[0] for pk in models.Supplier.objects.filter(is_deleted=False).values_list("id")]
            new_data = models.Warehouse(
                good_id=faker_en.ssn(),
                good_name=faker.name(),
                classification=models.Classification.objects.get(pk=random.choice(new_classification)),
                supplier=models.Supplier.objects.get(pk=random.choice(new_supplier))
            )
            if create_remark:
                new_data.remark = faker.text()
            new_data.save()
            increase_num -= 1


if __name__ == "__main__":

    import time
    import pytz

    TZ = pytz.timezone("Asia/Shanghai")
    # 进行数据的生成
    # create_data_classification()
    create_data_warehouse(60)

    # 在此下面进行数据的验证
    class_obj = models.Classification.objects.filter(is_deleted=False, class_name__icontains="james")
    # print(class_obj)

    # dt_time = datetime.datetime(*[int(i) for i in 时间.strip().split("-")], tzinfo=TZ)
    # dt_time = datetime.datetime(*(time.strptime("2019-05-25", "%Y-%m-%d")[0:6]), tzinfo=TZ)
    # print(dt_time)

    # ware_obj = models.Warehouse.objects.filter(
    #     is_deleted=False,
    #     supplier__supplier_id__icontains="3",
    #     classification__class_name__icontains="李",
    #     update_date__lte=dt_time
    # )

    # print(ware_obj)