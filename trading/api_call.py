import os
import time
import requests
from .models import CommodityPrice
from .db_interactions import delete_old_trades, handle_api_data


def call_the_api():
    """
    Api Call Function
    """
    # Check whether to get ships API
    ships = False

    # Time since last API call 3600 = 1 hour, 21600 = 6 hours
    time_in_seconds = 3600

    # Get the Date/Time in epoch format
    epoch_time = time.time()

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

    # Check if it's been more than * seconds since last update
    if epoch_time - time_in_seconds > last_update:

        # Increment the update number
        update_db = CommodityPrice.objects.get(code='UPDA')
        update_db.update += 1
        print("Update number:", update_db.update)
        update_db.save()

        # Set every tenth API call to update ships
        if (update_db.update % 10) == 0:
            ships = True

        # Check for any trades over 14 days old
        delete_old_trades()

        print("Last modified:", update_db.date_modified)
        print("Current Time:", epoch_time)
        print("Retrieving UEX API...")

        # Update last date modified in DB
        update_db.date_modified = int(epoch_time)
        update_db.save()

        if ships:
            api_url = "https://api.uexcorp.space/ships/"
        else:
            api_url = "https://api.uexcorp.space/commodities"

        # Connect to UEX API and get latest commodity prices
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
            handle_api_data(api_display, ships)
        else:
            # Tell the logs the API retrieve failed
            print(
                "API Retrieve Failed",
                api_response['code'],
                api_response['status'],
                time.ctime(epoch_time)
            )
        api_status = api_response['status']
    else:
        api_status = "na"

    return api_status
