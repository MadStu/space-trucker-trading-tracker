import os
import requests
from django.shortcuts import render

# Create your views here.

def index(request):

    API_URL = "https://api.uexcorp.space/systems"
    data = {
        "api_key": os.environ.get("UEX_API_KEY")
    }
    response = requests.post(API_URL, data)
    api_display = response.json()

    return render(request, "trading/index.html")
