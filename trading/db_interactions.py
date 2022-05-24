from .models import Trade, CommodityPrice, ErrorList


def handle_form_data(
    form_commodity,
    form_price,
    form_amount,
    form_buy,
    form_session,
    epoch_time
    ):
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

            # Work out stock cost and profit margin
            cost = float(form_amount) * float(form_price)
            entry.cost += int(cost)
            entry.profit += (
                float(form_amount) * cp_data.trade_price_sell
            ) - cost
        else:
            if int(form_amount) > entry.amount:
                # Sold more than is in cargo hold
                add_error_message("AMOUNT TOO HIGH", "TOP")
            else:
                entry.amount -= int(form_amount)

                # Work out stock cost and profit margin
                cost = float(form_amount) * cp_data.trade_price_buy
                entry.cost -= int(cost)
                entry.profit -= (
                    float(form_amount) * cp_data.trade_price_sell
                ) - cost
        # Update price paid and current time
        entry.price = form_price
        entry.time = epoch_time

        # Set whether trade was buy or sell, and for how many units
        entry.buy = form_buy
        entry.units = form_amount

        # Work out stock sell value
        entry.value = entry.amount * cp_data.trade_price_sell

        if not ErrorList.objects.exists():
            if entry.amount == 0:
                entry.delete()
            else:
                entry.save()

    else:
        # Work out stock sell value
        value = int(form_amount) * cp_data.trade_price_sell

        # Work out stock profit margin
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


















def add_error_message(message, location):
    ErrorList.objects.create(
        error_message=message,
        error_location=location
    )
    print(message)


def update_commodity_prices(request, commodity, buy, price, epoch_time):
    if not ErrorList.objects.exists() and request.user.is_superuser:
        cp_data = CommodityPrice.objects.get(name=commodity)

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
            add_error_message("PRICE WAS NOT CORRECT", "TOP")

        # If no errors, save the data
        if not ErrorList.objects.exists():
            cp_data.save()
