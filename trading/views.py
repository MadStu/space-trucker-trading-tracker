from django.shortcuts import render
from .models import Trade

# Create your views here.

def index(request):
    items = Trade.objects.all()
    context = {
        'items': items,
        'api': Trade.api_display,
        'data': Trade.data
    }
    return render(request, "trading/index.html", context)
