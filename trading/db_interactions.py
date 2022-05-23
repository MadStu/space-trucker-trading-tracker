import requests
from .models import Trade, CommodityPrice, ErrorList

def add_error_message(message, location):
    ErrorList.objects.create(
        error_message=message,
        error_location=location
    )
    print(message)
