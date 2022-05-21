import os
import requests
from django.db import models


class Trade(models.Model):
    commodity = models.CharField(max_length=50, null=False, blank=False)
    price = models.FloatField()
    amount = models.IntegerField()
    buy = models.BooleanField(null=False, blank=False, default=False)

    # Connect to UEX API and get latest commodity prices
    API_URL = "https://api.uexcorp.space/commodities"
    data = {
        "api_key": os.environ.get("UEX_API_KEY")
    }
    response = requests.get(API_URL, headers=data)
    api_response = response.json()

    # Check API is working
    if api_response['code'] == 200:
        api_display = api_response['data']
    else:
        api_display = [
            {
            "code": "ERRR",
            "name": f"Response Code: {api_response['code']}",
            "kind": "ERROR",
            "trade_price_buy": 1,
            "trade_price_sell": 1000,
            "date_added": 1,
            "date_modified": 1
            }
        ]

    # Create a new list
    newlist = []
    for item in api_display:
        item['profit'] = round(item['trade_price_sell'] - item['trade_price_buy'], 2)

        # Only add tradeable commodities to the new list
        if item['kind'] != 'Temporary' and item['kind'] != 'Drug':
            if item['trade_price_buy'] > 0.01 and item['trade_price_sell'] > 0.01:
                newlist.append(item)

    def __str__(self):
        return self.commodity
