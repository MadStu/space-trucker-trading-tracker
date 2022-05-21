from django.shortcuts import render
from .models import Trade

# Create your views here.

def index(request):
    trades = Trade.objects.all()
    context = {
        'api': Trade.commodity_data,
        'com': Trade.commodity,
        'trades': trades
    }
    return render(request, "trading/index.html", context)
