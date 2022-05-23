import os
import time
import requests
from django.shortcuts import render, redirect
from .models import Trade, CommodityPrice


def index(request):
    # Get the Date/Time in epoch format
    epoch_time = time.time()
    update_db = CommodityPrice.objects.get(code='UPDA')
    last_update = update_db.date_modified

    # Check if it's been more than * hours since last update
    # 3600 = 1 hour, 21600 = 6 hours
    if epoch_time - 21600 > last_update:
        print("Last modified:", update_db.date_modified)
        print("Current Time:", epoch_time)
        print("Retrieving UEX API...")

        # Update last date modified in DB
        update_db.date_modified = int(epoch_time)
        update_db.save()

        # Connect to UEX API and get latest commodity prices
        api_url = "https://api.uexcorp.space/commodities"
        headers = {"api_key": os.environ.get("UEX_API_KEY")}
        response = requests.get(api_url, headers=headers)
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

    # Create a new list from the database
    commodity_data = []
    for item in CommodityPrice.objects.values():
        # Only add legal tradeable commodities to the new list
        if item['profit'] > 0 and item['kind'] != 'Drug':
            if item['trade_price_buy'] > 0:
                commodity_data.append(item)

    # Handle Form posts to add or edit a trade in the database
    if request.method == 'POST':
        form_commodity = request.POST.get('form_commodity')
        form_price = request.POST.get('form_price')
        form_amount = request.POST.get('form_amount')
        form_buy = True if request.POST.get('form_buy') == "True" else False

        # Get the object from the database
        entry = Trade.objects.get(commodity=form_commodity)

        if entry.commodity == form_commodity:
            # Update existing trade details
            if form_buy:
                entry.amount = entry.amount + int(form_amount)
            else:
                entry.amount = entry.amount - int(form_amount)
            entry.price = form_price
            entry.save()
        else:
            # Insert new trade
            Trade.objects.create(
                commodity=form_commodity,
                price=form_price,
                amount=form_amount,
                buy=form_buy
            )

        # retrieve CommodityPrice data
        entry = CommodityPrice.objects.get(name=form_commodity)

        # Update existing prices to CommodityPrice
        if entry.name == form_commodity:
            if form_buy:
                # Update if Buying
                entry.trade_price_buy = float(form_price)
            else:
                # Update if Selling
                entry.trade_price_sell = float(form_price)
            entry.profit = round(
                entry.trade_price_sell - entry.trade_price_buy, 2)
            entry.date_modified = int(epoch_time)
            entry.save()
            print("Commodity Updated:", item['code'])

        return redirect('index')

    trades = Trade.objects.all()
    context = {
        'commodity_data': commodity_data,
        'com': Trade.commodity,
        'trades': trades,
        'time_now': time.ctime(epoch_time),
        'last_updated': time.ctime(last_update)
    }

    return render(request, "trading/index.html", context)
