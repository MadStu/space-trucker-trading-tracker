from django.shortcuts import render
from .models import Trade

# Create your views here.

def index(request):
    context = {
        'api': Trade.api_display
    }
    return render(request, "trading/index.html", context)
