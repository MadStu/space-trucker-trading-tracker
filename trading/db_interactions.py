import time
from django.contrib import messages
from .models import Trade, CommodityPrice, ErrorList, UserProfit, ShipList


def handle_form_data(
    form_commodity,
    form_price,
    form_amount,
    form_buy,
    form_session,
    epoch_time,
    request,
    ship_code,
    commodity_code
):
    """
    Handles the data received submitted on the form
    """
    error_message = None

    # Retrieve CommodityPrice data
    cp_data = CommodityPrice.objects.get(name=form_commodity)

    # Check if the trade exists in the database
    if Trade.objects.filter(
        commodity=form_commodity,
        session=form_session
    ).exists():

        # Get the object from the database
        entry = Trade.objects.get(
            commodity=form_commodity,
            session=form_session
        )

        # Update existing trade details
        if form_buy:
            entry.amount += int(form_amount)

            # Work out stock cost and potential profit margin
            cost = float(form_amount) * float(form_price)
            entry.cost += int(cost)
            entry.profit += (
                float(form_amount) * cp_data.trade_price_sell
            ) - cost
            cost_amount = cost

        else:
            if int(form_amount) > entry.amount:
                # Sold more than is in cargo hold
                msg = "You've tried to sell more cargo than you have in stock."
                error_message = msg
            else:
                entry.amount -= int(form_amount)

                # Work out stock cost and profit margin
                cost = float(form_amount) * cp_data.trade_price_buy
                entry.cost -= int(cost)
                entry.profit -= (
                    float(form_amount) * cp_data.trade_price_sell
                ) - cost
                cost_amount = float(form_amount) * cp_data.trade_price_sell
                cost_amount = float(form_amount) * float(form_price)

        # Update price paid and current time
        entry.price = form_price
        entry.time = epoch_time

        # Set whether trade was buy or sell, and for how many units
        entry.buy = form_buy
        entry.units = form_amount

        # Work out potential stock sell value
        entry.value = entry.amount * cp_data.trade_price_sell

        if error_message is not None:
            add_error_message(error_message, form_session)
        else:
            if entry.amount < 1:
                entry.delete()
            else:
                entry.save()
            # Save UserProfit data
            user_profit_calc(form_session, cost_amount, form_buy, ship_code, commodity_code)
            msg = "Trade successfully added."
            # messages.add_message(request, messages.SUCCESS, msg)

    else:
        # No stock of this commodity on board so create a new record

        # Check it's a buy trade
        if form_buy:

            # Work out stock sell value
            value = int(form_amount) * cp_data.trade_price_sell

            # Work out potential stock profit margin
            cost = float(form_amount) * float(form_price)
            profit = (float(form_amount) * cp_data.trade_price_sell) - cost

            # Insert new trade
            Trade.objects.create(
                commodity=form_commodity,
                price=form_price,
                amount=form_amount,
                cost=cost,
                value=value,
                profit=profit,
                session=form_session,
                time=epoch_time,
                buy=form_buy,
                units=form_amount
            )
            # Save UserProfit data
            user_profit_calc(form_session, cost, form_buy, ship_code, commodity_code)
            msg = "Trade successfully added."
            # messages.add_message(request, messages.SUCCESS, msg)
        else:
            # Trying to sell something with 0 stock so send a message.
            add_error_message(
                "You've tried to sell more cargo than you have in stock.",
                form_session
            )


def update_commodity_prices(
    request,
    commodity,
    buy,
    price,
    sell,
    editor,
    epoch_time,
    session_key
):
    """
    Updates the Commodity prices if the user is an admin
    """

    if request.user.is_superuser:
        error_message = None

        cp_data = CommodityPrice.objects.get(name=commodity)

        if editor:
            # Update existing prices to CommodityPrice
            cp_data.trade_price_buy = float(price)
            cp_data.trade_price_sell = float(sell)
        else:
            # Update existing prices to CommodityPrice
            if buy:
                # Update if Buying
                cp_data.trade_price_buy = float(price)
            else:
                # Update if Selling
                cp_data.trade_price_sell = float(price)

        # Calculate profit from new price values
        cp_data.profit = round(
            cp_data.trade_price_sell - cp_data.trade_price_buy, 2)
        cp_data.date_modified = int(epoch_time)

        # Check for errors
        if cp_data.profit < 0.01:
            error_message = "The price you entered would not make a profit."

        # If no errors, save the data
        if error_message is not None:
            add_error_message(error_message, session_key)
        else:
            # Check no errors before updating
            if not ErrorList.objects.filter(session=session_key).exists():
                cp_data.save()
                msg = "Commodity successfully updated."
                messages.add_message(request, messages.SUCCESS, msg)


def add_error_message(message, session):
    """
    Inserts an error message into the database
    """
    ErrorList.objects.create(
        error_message=message,
        session=session
    )
    print(message)


def commodity_data():
    """
    Returns a list with the tradeable commodity data
    """
    # Create a new list from the database
    commodity_data_list = []
    for item in CommodityPrice.objects.values():
        # Only add legal tradeable commodities to the new list
        if item['profit'] > 0 and item['kind'] != 'Drug':
            if item['trade_price_buy'] > 0 and item['kind'] != 'Temporary':
                item['date'] = time.ctime(item['date_modified'])
                commodity_data_list.append(item)
    return commodity_data_list


def user_profit_calc(session, cost, buy, ship_code, commodity_code):
    """
    Handle the UserProfit queries
    """
    # Check if record exists
    if not UserProfit.objects.filter(session=session).exists():

        # Insert new record
        UserProfit.objects.create(
            session=session,
            profit=0,
            ship_code=ship_code,
            commodity_code=commodity_code
        )

    # Retrieve UserProfit data
    up_data = UserProfit.objects.get(session=session)

    up_data.ship_code = ship_code
    up_data.commodity_code = commodity_code

    if buy:
        up_data.profit -= int(cost)
    else:
        up_data.profit += int(cost)

    up_data.save()


def delete_old_trades():
    """
    Remove trades over 14 days old

    function called at the same time as the API (no sooner than every 6 hours)
    """
    # Get time in second
    epoch_time = time.time()

    # Define how many seconds to allow trade to exist
    # 86400 = 1 day, 1209600 = 14 days
    days_in_seconds = 1209600

    trades = Trade.objects.all()

    for trade in trades:
        if trade.time < epoch_time - days_in_seconds:
            trade.delete()


def delete_old_commodity():
    """
    Remove defunct commodities
    """
    # Get Commodity data
    update_db = CommodityPrice.objects.get(code='UPDA')
    commodities = CommodityPrice.objects.all()

    # Delete commodity if older than 12 API cycles
    for commodity in commodities:
        if commodity.update < update_db.update - 12:
            print("Deleting Comodity:", commodity.name)
            commodity.delete()


def ship_data():
    """
    Returns a list of ships currently capable of trade
    """
    # Create a new list from the database
    ship_data_list = []
    for item in ShipList.objects.values():
        # Only add legal tradeable commodities to the new list
        if item['units'] > 0 and item['implemented'] == 1:
            ship_data_list.append(item)
    return ship_data_list
