import os
import requests
import time
from django.shortcuts import render
from .models import Trade, CommodityPrice


def index(request, *args, **kwargs):

    epoch_time = time.time()
    update_db = CommodityPrice.objects.get(code='UPDA')
    last_update = update_db.date_modified

    # Check if it's been more than 1 hour since last update
    # 3600 = 1 hour
    if epoch_time - 3600 > last_update:
        print("Last modified:", update_db.date_modified)
        print("Current Time:", epoch_time)
        print("Retrieving UEX API...")

        # Date last modified updated in DB
        update_db.date_modified = int(epoch_time)
        update_db.save()

        # Connect to UEX API and get latest commodity prices
        API_URL = "https://api.uexcorp.space/commodities"
        data = {"api_key": os.environ.get("UEX_API_KEY")}
        response = requests.get(API_URL, headers=data)
        api_response = response.json()

        # Check API is working
        if api_response['code'] == 200:
            api_display = api_response['data']
            print(
                "API Retrieve Successful",
                api_response['code'],
                api_response['status']
            )

            for item in api_display:
                # Calculate the profit and round down to 2 decimal places
                item['profit'] = round(
                    item['trade_price_sell'] - item['trade_price_buy'], 2)

                # Update Database
                if CommodityPrice.objects.filter(code=item['code']).exists():
                    entry = CommodityPrice.objects.get(code=item['code'])

                    # Check if API data is newer than the DB entry
                    if item['date_modified'] > entry.date_modified:

                        # Update existing details
                        entry.code = item['code']
                        entry.name = item['name']
                        entry.kind = item['kind']
                        entry.trade_price_buy = item['trade_price_buy']
                        entry.trade_price_sell = item['trade_price_sell']
                        entry.date_modified = item['date_modified']
                        entry.profit = item['profit']
                        entry.save()
                        print("Commodity Updated:", item['code'])

                else:
                    # Insert new commodity
                    CommodityPrice.objects.create(
                        code=item['code'],
                        name=item['name'],
                        kind=item['kind'],
                        trade_price_buy=item['trade_price_buy'],
                        trade_price_sell=item['trade_price_sell'],
                        date_modified=item['date_modified'],
                        profit=item['profit']
                    )
                    print("Commodity Inserted:", item['code'])
        else:
            print(
                "API Retrieve Failed",
                api_response['code'],
                api_response['status']
            )

    # Create a new list from the database.....
    commodity_data = []

    for item in CommodityPrice.objects.values():
        # Only add legal tradeable commodities to the new list
        if item['profit'] > 0 and item['kind'] != 'Drug':
            if item['trade_price_buy']:
                commodity_data.append(item)

    trades = Trade.objects.all()
    context = {
        'api': commodity_data,
        'com': Trade.commodity,
        'trades': trades,
        'time_now': time.ctime(epoch_time),
        'last_updated': time.ctime(last_update)
    }

    return render(request, "trading/index.html", context)
