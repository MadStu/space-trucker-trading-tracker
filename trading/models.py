import os
import requests
from django.db import models


class Trade(models.Model):
    commodity = models.CharField(max_length=50, null=False, blank=False)
    price = models.FloatField()
    amount = models.IntegerField()
    buy = models.BooleanField(null=False, blank=False, default=False)

    API_URL = "https://api.uexcorp.space/commodities"
    data = {
        "api_key": os.environ.get("UEX_API_KEY")
    }
    response = requests.get(API_URL, headers=data)
    api_display = response.json()

    def __str__(self):
        return self.commodity
