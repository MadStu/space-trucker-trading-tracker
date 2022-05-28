import os
import time
import requests
from django.shortcuts import render, redirect
from django.db.models import Max
from .models import Trade, CommodityPrice, ErrorList, UserProfit
from .db_interactions import update_commodity_prices, handle_form_data
from .db_interactions import handle_api_data, commodity_data


def index(request):
    """
    The main index page where the magic happens
    """
    global form_commodity
    global form_price
    global form_amount
    global form_buy

    # Time since last API call 3600 = 1 hour, 21600 = 6 hours
    time_in_seconds = 21600

    # Get the Date/Time in epoch format
    epoch_time = time.time()

    # Get the last API update time
    update_db = CommodityPrice.objects.get(code='UPDA')
    last_update = update_db.date_modified

    # Seconds to make 930 years from now (the current timezone in Star Citizen)
    sc_time = 29348006400

    # Friendly Star Citizen date formats
    time_now = time.strftime(
        '%B %-d, %Y %H:%M:%S',
        time.localtime(epoch_time+sc_time)
    )
    last_updated = time.strftime(
        '%B %-d, %Y %H:%M:%S',
        time.localtime(last_update+sc_time)
    )

    # Retrieve either a unique session key or the user details
    session_key = request.session._get_or_create_session_key()
    if request.user.is_authenticated:
        session_key = request.user.username

    # Check if it's been more than * hours since last update
    # 3600 = 1 hour, 21600 = 6 hours
    if epoch_time - time_in_seconds > last_update:
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
            # Handle the API data in db_interactions
            handle_api_data(api_display)
        else:
            # Tell the logs the API retrieve failed
            print(
                "API Retrieve Failed",
                api_response['code'],
                api_response['status'],
                time.ctime(epoch_time)
            )

    # Handle the received Form data
    if request.method == 'POST':
        form_session = request.POST.get('session_key')
        if request.POST.get('reset_profit'):
            if UserProfit.objects.filter(session=form_session).exists():
                up_data = UserProfit.objects.get(session=form_session)
                up_data.profit = 0
                up_data.save()
        else:
            form_buy = True if request.POST.get('form_buy') == "True" else False

            if form_buy:
                form_commodity = request.POST.get('form_buy_commodity')
                form_price = request.POST.get('form_buy_price')
                form_amount = int(request.POST.get('form_buy_amount'))
            else:
                form_commodity = request.POST.get('form_sell_commodity')
                form_price = request.POST.get('form_sell_price')
                form_amount = int(request.POST.get('form_sell_amount'))

            # Insert the form data in db_interactions
            handle_form_data(
                form_commodity,
                form_price,
                form_amount,
                form_buy,
                form_session,
                epoch_time
            )

            # Update CommodityPrice data in db_interactions
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

    # Calculate the totals for display
    trades = Trade.objects.all().filter(session=session_key)
    total_cargo = 0
    total_value = 0
    total_profit = 0
    total_cost = 0
    for trade in trades:
        total_cargo += trade.amount
        total_value += trade.value
        total_profit += trade.profit
        total_cost += trade.cost

    # Get currently trading profit
    if UserProfit.objects.filter(session=session_key).exists():
        up_data = UserProfit.objects.get(session=session_key)
        user_profit = up_data.profit
    else:
        user_profit = 0

    errors = ErrorList.objects.all()
    ErrorList.objects.all().delete()
    context = {
        'commodity_data': commodity_data(),  # List from db_interactions
        'com': Trade.commodity,
        'trades': trades,
        'time_now': time_now,
        'last_updated': last_updated,
        'session_key': session_key,
        'errors': errors,
        'total_cargo': total_cargo,
        'total_value': round(total_value),
        'total_profit': round(total_profit+user_profit+total_cost),
        'total_cost': round(total_cost),
        'populate_commodity': form_commodity,
        'populate_price': float(form_price),
        'populate_amount': int(form_amount),
        'populate_buy': form_buy,
        'user_profit': int(user_profit)
    }

    return render(request, "trading/index.html", context)


def editor(request):
    """
    The price editor page for use only by the admins
    """
    epoch_time = time.time()

    # Handle the received Form data
    if request.method == 'POST':
        form_buy_price = request.POST.get('form_buy_price')
        form_sell_price = request.POST.get('form_sell_price')
        commodity_id = request.POST.get('commodity_id')

        cp_data = CommodityPrice.objects.get(code=commodity_id)

        cp_data.trade_price_buy = float(form_buy_price)
        cp_data.trade_price_sell = float(form_sell_price)
        cp_data.date_modified = int(epoch_time)

        cp_data.save()

    context = {
        'commodity_data': commodity_data(),
    }
    return render(request, "trading/editor.html", context)


def prices(request):
    """
    The price viewer page is to show the current prices
    """
    context = {
        'commodity_data': commodity_data(),
    }
    return render(request, "trading/prices.html", context)
