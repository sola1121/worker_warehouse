import os

from django.apps import AppConfig

default_app_config = "warehouse.WarehouseConfig"

def get_current_app_name(_file):
    return os.path.split(os.path.dirname(_file))[-1]


class WarehouseConfig(AppConfig):
    name = get_current_app_name(__file__)
    verbose_name = "仓储数据"
