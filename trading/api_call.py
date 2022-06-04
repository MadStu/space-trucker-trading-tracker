from pathlib import Path
import os
import time
import requests
from .db_interactions import delete_old_trades, delete_old_commodity
from .models import CommodityPrice, ShipList


path_to_file = 'vars.py'
path = Path(path_to_file)

if path.is_file():
    from vars import UEX_API_KEY, UPDATE_TIME
else:
    UEX_API_KEY = os.environ.get('UEX_API_KEY')
    UPDATE_TIME = os.environ.get('UPDATE_TIME')


def call_the_api():
    """
    Api Call Function
    """
    # Check whether to get ships API
    ships = False

    # Time since last API call 3600 = 1 hour, 21600 = 6 hours
    time_in_seconds = int(UPDATE_TIME)

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
        headers = {"api_key": UEX_API_KEY}
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


def handle_api_data(api_display, ships):
    """
    Handles the data received by the API
    """
    # Loop through the records
    for item in api_display:
        if not ships:
            # Not ships so must be a commodity update
            # Calculate the profit and round down to 2 decimal places
            item['profit'] = round(
                item['trade_price_sell'] - item['trade_price_buy'], 2)

            update_db = CommodityPrice.objects.get(code='UPDA')

            # Check if the record exists
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

                # Sync the update number
                entry.update = update_db.update

                # Save the updated record
                entry.save()
            else:
                # Doesn't exist so insert new commodity
                CommodityPrice.objects.create(
                    code=item['code'],
                    name=item['name'],
                    kind=item['kind'],
                    trade_price_buy=item['trade_price_buy'],
                    trade_price_sell=item['trade_price_sell'],
                    date_modified=item['date_modified'],
                    profit=item['profit'],
                    update=update_db.update
                )
        else:
            # Update Ships
            # Check if the record exists
            if ShipList.objects.filter(code=item['code']).exists():
                entry = ShipList.objects.get(code=item['code'])

                # Check if API data is newer than the DB entry
                if item['date_modified'] > entry.date_modified:
                    # Update existing details
                    entry.code = item['code']
                    entry.name = item['name']
                    entry.units = (int(item['scu'])*100)
                    entry.date_modified = item['date_modified']
                    entry.implemented = item['implemented']
                    entry.save()
            else:
                # Doesn't exist so insert new ship
                ShipList.objects.create(
                    code=item['code'],
                    name=item['name'],
                    units=(int(item['scu'])*100),
                    date_modified=item['date_modified'],
                    implemented=int(item['implemented'])
                )
    # Delete old commodities after API handling has completed
    delete_old_commodity()
