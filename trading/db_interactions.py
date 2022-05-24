#import requests
from .models import Trade, CommodityPrice, ErrorList

def add_error_message(message, location):
    ErrorList.objects.create(
        error_message=message,
        error_location=location
    )
    print(message)

def update_commodity_prices(commodity, buy, price, epoch_time):

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
