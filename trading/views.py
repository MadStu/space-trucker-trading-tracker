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

    # Set error message to blank
    error_message = []
    form_error = ''

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
                api_response['status'],
                time.ctime(epoch_time)
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
            # Tell the logs the API retrieve failed
            print(
                "API Retrieve Failed",
                api_response['code'],
                api_response['status'],
                time.ctime(epoch_time)
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
        form_error = request.POST.get('error_message')
        form_buy = True if request.POST.get('form_buy') == "True" else False

        # Check if the trade exists in the database
        if Trade.objects.filter(commodity=form_commodity).exists():

            # Get the object from the database
            entry = Trade.objects.get(commodity=form_commodity)

            # Update existing trade details
            if form_buy:
                entry.amount = entry.amount + int(form_amount)
            else:
                if int(form_amount) > entry.amount:
                    # Sold more than is in cargo hold
                    error_message.append("AMOUNT TOO HIGH")
                    print(error_message, "1")
                else:
                    entry.amount = entry.amount - int(form_amount)
            entry.price = form_price
            if not error_message:
                entry.save()
        else:
            # Insert new trade if there isn't one with that commodity
            Trade.objects.create(
                commodity=form_commodity,
                price=form_price,
                amount=form_amount,
                buy=form_buy
            )

        # Retrieve CommodityPrice data
        entry = CommodityPrice.objects.get(name=form_commodity)

        if not error_message:
            # Update existing prices to CommodityPrice
            if form_buy:
                # Update if Buying
                entry.trade_price_buy = float(form_price)
            else:
                # Update if Selling
                entry.trade_price_sell = float(form_price)
            entry.profit = round(
                entry.trade_price_sell - entry.trade_price_buy, 2)
            entry.date_modified = int(epoch_time)

            if entry.profit < 0.01:
                error_message.append("PRICE WAS NOT CORRECT")

            if not error_message:
                entry.save()
                print("Commodity Updated:", item['code'])

        return redirect('index')

    # print(error_message, "2")
    # if form_error:
    #     form_error = f"- - - - - ERROR: {form_error} - - - - -"
    print(error_message, "3")
    

    trades = Trade.objects.all()
    context = {
        'commodity_data': commodity_data,
        'com': Trade.commodity,
        'trades': trades,
        'time_now': time.ctime(epoch_time),
        'last_updated': time.ctime(last_update),
        'error_message': form_error
    }

    return render(request, "trading/index.html", context)
