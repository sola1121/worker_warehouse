from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Create your views here.

def index(request):
    return render(request, "app_index/index.html", {"active_navbar": "index"})
