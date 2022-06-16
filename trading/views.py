import time
from django.shortcuts import render, redirect
from django.db.models import Max
from django.contrib import messages
from .models import Trade, CommodityPrice, ErrorList, UserProfit
from .db_interactions import update_commodity_prices, handle_form_data
from .db_interactions import commodity_data, ship_data, add_error_message
from .api_call import call_the_api


def index(request):
    """
    The main index page where the magic happens
    """
    # Get the Date/Time in epoch format
    epoch_time = time.time()

    # Seconds to make 930 years from now (the current timezone in Star Citizen)
    sc_time = 29348006400

    # Retrieve either a unique session key or the user details
    session_key = request.session._get_or_create_session_key()
    if request.user.is_authenticated:
        session_key = str(request.user.id)

    # Get the last API update time
    if CommodityPrice.objects.filter(code='UPDA').exists():
        update_db = CommodityPrice.objects.get(code='UPDA')
        last_update = update_db.date_modified

    else:
        # Doesn't exist so insert new Update entry
        CommodityPrice.objects.create(
            code='UPDA',
            name='Time Updated',
            kind='Epoch Time',
            trade_price_buy=0,
            trade_price_sell=0,
            date_modified=0,
            profit=0
        )
        update_db = CommodityPrice.objects.get(code='UPDA')
        last_update = 0

    # Friendly Star Citizen date formats
    time_now = time.strftime(
        '%B %-d, %Y %H:%M:%S',
        time.localtime(epoch_time+sc_time)
    )
    last_updated = time.strftime(
        '%B %-d, %Y %H:%M:%S',
        time.localtime(last_update+sc_time)
    )

    # Handle the received Form data
    if request.method == 'POST':
        form_session = request.POST.get('session_key')

        if request.POST.get('clear_errors'):
            # Delete this user's errors so they don't get displayed again
            ErrorList.objects.all().filter(session=session_key).delete()
        elif str(session_key) != str(form_session):
            # Check both IDs match to verify
            msg = "Session IDs do not match, please register or log in."
            add_error_message(msg, session_key)

        elif request.POST.get('reset_profit'):
            if UserProfit.objects.filter(session=form_session).exists():
                up_data = UserProfit.objects.get(session=form_session)
                up_data.profit = 0
                up_data.save()
                msg = "Profit successfully reset."
                # messages.add_message(request, messages.SUCCESS, msg)
        else:
            if request.POST.get('form_buy') == "True":
                form_buy = True
            else:
                form_buy = False

            if form_buy:
                form_commodity = request.POST.get('form_buy_commodity')
                form_price = request.POST.get('form_buy_price')
                form_amount = int(request.POST.get('form_buy_amount'))
            else:
                form_commodity = request.POST.get('form_sell_commodity')
                form_price = request.POST.get('form_sell_price')
                form_amount = int(request.POST.get('form_sell_amount'))
            ship = request.POST.get('ship_data')
            commodity_code = request.POST.get('commodity_code')

            # Insert the form data in db_interactions
            handle_form_data(
                form_commodity,
                form_price,
                form_amount,
                form_buy,
                form_session,
                epoch_time,
                request,
                ship,
                commodity_code
            )

            # Update CommodityPrice data in db_interactions
            update_commodity_prices(
                request,
                form_commodity,
                form_buy,
                form_price,
                0,
                False,
                epoch_time,
                form_session
            )
            return redirect('index')

    # Get currently trading profit
    if UserProfit.objects.filter(session=session_key).exists():
        up_data = UserProfit.objects.get(session=session_key)
        user_profit = up_data.profit
        user_ship = up_data.ship_code
        form_commodity = up_data.commodity_code
    else:
        user_profit = 0
        user_ship = "CATERP"
        form_commodity = "Gold"

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
        form_price = 27.83
        form_amount = 69600
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

    error_list = ErrorList.objects.all().filter(session=session_key)
    context = {
        'commodity_data': commodity_data(),  # List from db_interactions
        'com': Trade.commodity,
        'trades': trades,
        'time_now': time_now,
        'last_updated': last_updated,
        'session_key': session_key,
        'total_cargo': total_cargo,
        'total_value': round(total_value),
        'total_profit': round(total_profit+user_profit+total_cost),
        'total_cost': round(total_cost),
        'populate_commodity': form_commodity,
        'populate_price': Decimal(form_price),
        'populate_amount': int(form_amount),
        'populate_buy': form_buy,
        'user_profit': int(user_profit),
        'error_list': error_list,
        'ships': ship_data(),
        'user_ship': user_ship
    }

    return render(request, "trading/index.html", context)


def editor(request):
    """
    The price editor page for use only by the admins
    """
    epoch_time = time.time()

    # Retrieve either a unique session key or the user details
    session_key = request.session._get_or_create_session_key()
    if request.user.is_authenticated:
        session_key = str(request.user.id)

    # Handle the received Form data
    if request.method == 'POST':
        form_buy_price = request.POST.get('form_buy_price')
        form_sell_price = request.POST.get('form_sell_price')
        commodity_id = request.POST.get('commodity_id')

        update_commodity_prices(
            request,
            commodity_id,
            None,
            form_buy_price,
            form_sell_price,
            True,
            epoch_time,
            session_key
        )

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


def usage(request):
    """
    Shows the user how to use the STTT
    """
    return render(request, "trading/usage.html")


def api_call(request):
    """
    Calls the api function to update commodity prices
    """
    context = {
        'api_call': call_the_api()
    }

    return render(request, "trading/apicall.html", context)


def error_400(request, exception):
    """"
    Shows page for a 400 Error
    """
    # Retrieve either a unique session key or the user details
    session_key = request.session._get_or_create_session_key()
    if request.user.is_authenticated:
        session_key = str(request.user.id)

    msg = "400 Error! It looks like you've sent a bad request :("
    add_error_message(msg, session_key)
    error_list = ErrorList.objects.all().filter(session=session_key)
    context = {
        'error_list': error_list
    }
    return render(request, 'trading/index.html', context)


def error_403(request, exception):
    """"
    Shows page for a 403 Error
    """
    # Retrieve either a unique session key or the user details
    session_key = request.session._get_or_create_session_key()
    if request.user.is_authenticated:
        session_key = str(request.user.id)

    msg = "403 Error! RESTRICTED AREA!"
    add_error_message(msg, session_key)
    error_list = ErrorList.objects.all().filter(session=session_key)
    context = {
        'error_list': error_list
    }
    return render(request, 'trading/index.html', context)


def error_404(request, exception):
    """"
    Shows page for a 404 Error
    """
    # Retrieve either a unique session key or the user details
    session_key = request.session._get_or_create_session_key()
    if request.user.is_authenticated:
        session_key = str(request.user.id)

    msg = "404 Error! You're lost in space. This page doesn't exist!"
    add_error_message(msg, session_key)
    error_list = ErrorList.objects.all().filter(session=session_key)
    context = {
        'error_list': error_list
    }
    return render(request, 'trading/index.html', context)


def error_500(request):
    """"
    Shows page for a 500 Error
    """
    # Retrieve either a unique session key or the user details
    session_key = request.session._get_or_create_session_key()
    if request.user.is_authenticated:
        session_key = str(request.user.id)

    msg = "500 Error! Server error! Our own little 30k :("
    add_error_message(msg, session_key)
    error_list = ErrorList.objects.all().filter(session=session_key)
    context = {
        'error_list': error_list
    }
    return render(request, 'trading/index.html', context)
