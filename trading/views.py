import os
import time
import requests
from django.shortcuts import render, redirect
from django.db.models import Max
from .models import Trade, CommodityPrice, ErrorList
from .db_interactions import update_commodity_prices, handle_form_data


def index(request):
    global form_commodity
    global form_price
    global form_amount
    global form_buy

    # Retrieve either a unique session key or the user details
    session_key = request.session._get_or_create_session_key()
    if request.user.is_authenticated:
        session_key = request.user.username

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
        form_amount = int(request.POST.get('form_amount'))
        form_buy = True if request.POST.get('form_buy') == "True" else False
        form_session = request.POST.get('session_key')

        # Insert the form data
        handle_form_data(
            form_commodity,
            form_price,
            form_amount,
            form_buy,
            form_session,
            epoch_time
        )

        # Update CommodityPrice data
        update_commodity_prices(
            request,
            form_commodity,
            form_buy,
            form_price,
            epoch_time
        )

        return redirect('index')

    # Get the user's last trade to retrieve the values
    # Check if user has a trade entry
    if Trade.objects.filter(
        session=session_key
    ).exists():
        # Get the most recent object from the database
        latest_trade = Trade.objects.filter(
            session=session_key
        ).aggregate(time=Max('time'))['time']
        entry = Trade.objects.get(session=session_key, time=latest_trade)

        # Send the values to the index page
        form_commodity = entry.commodity
        form_price = entry.price
        form_amount = entry.units
        form_buy = entry.buy
    else:
        # Default values
        form_commodity = "Laranite"
        form_price = 27.83
        form_amount = 5000
        form_buy = True

    trades = Trade.objects.all().filter(session=session_key)

    # Calculate the totals for display
    total_cargo = 0
    total_value = 0
    total_profit = 0
    total_cost = 0
    for trade in trades:
        total_cargo += trade.amount
        total_value += trade.value
        total_profit += trade.profit
        total_cost += trade.cost

    errors = ErrorList.objects.all()
    ErrorList.objects.all().delete()
    context = {
        'commodity_data': commodity_data,
        'com': Trade.commodity,
        'trades': trades,
        'time_now': time.ctime(epoch_time),
        'last_updated': time.ctime(last_update),
        'session_key': session_key,
        'errors': errors,
        'total_cargo': total_cargo,
        'total_value': round(total_value),
        'total_profit': round(total_profit),
        'total_cost': round(total_cost),
        'populate_commodity': form_commodity,
        'populate_price': float(form_price),
        'populate_amount': int(form_amount),
        'populate_buy': form_buy
    }

    return render(request, "trading/index.html", context)
