from django.shortcuts import render
from django.contrib.auth.decorators import login_required

from account.models import User, History, Notification
from warehouse.models import Supplier, Classification, InWarehouse, OutWareHouse, Warehouse, Sale

# Create your views here.

@login_required(login_url="/")
def index(request):
    
    return render(request, 
                  "app_index/index.html", 
                  {"active_navbar": "index",
                  })
