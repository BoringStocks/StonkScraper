from src import app
from .robinhood import Robinhood
import json
from datetime import datetime
import traceback
from flask_api import status

# https://github.com/jmfernandes/robin_stocks
# http://www.robin-stocks.com/en/latest/robinhood.html#getting-stock-information


@app.route('/v2/<ticker>')
def get_all_v2(ticker):
    print(f'{ticker} requested at {datetime.utcnow()}')

    # Detect if json exists, create new json if none found
    try:
        # Unpack old json to parse time
        with open('data.json', 'r') as data_json:
            old_json = json.load(data_json)

        # Determine difference between old/new timestamps
        format = "%H:%M:%S"
        old_time = old_json['timestamp']
        old_price = old_json['current']
        new_time = (datetime.utcnow()).strftime(format)
        time_delta = datetime.strptime(
            new_time, format) - datetime.strptime(old_time, format)

        # Return new scrape if difference in stamps exceeds 5 secs or new index is requested
        if abs(time_delta.total_seconds()) >= 5 or old_json['symbol'] != ticker.upper():

            # return new current, write new data into json
            print('Returning new scrape')

            data = Robinhood.get_ticker(ticker)

            # catch bad index
            if not data:
                return f'{ticker} not found', status.HTTP_400_BAD_REQUEST
            
            # Calculate points change
            data['points_change'] = round(float(data['current'] - old_price), 2)

            # Write payload to json
            with open('data.json', 'w') as new_unpacked_json:
                json.dump(data, new_unpacked_json)

            return data

        else:
            # return old data if timestamp difference less than 5 secs
            print('Returning old scrape')
            return old_json

    except Exception as error:
        traceback.print_exc()

        # Run if no JSON found
        print('No JSON found, creating new JSON with requested index')

        data = Robinhood.get_ticker(ticker)
        print(data)

        if not data:
            return f'{ticker} not found', status.HTTP_400_BAD_REQUEST

        # Write scrape to new json
        with open('data.json', 'w') as data_json:
            json.dump(data, data_json)

        return data


@app.route('/v2/<ticker>/historical/<data_range>')
def get_historical_v2(ticker, data_range):
    historical_data = Robinhood.get_historical(
        ticker, data_range)

    if not historical_data:
        return f'{ticker} not found', status.HTTP_400_BAD_REQUEST

    return historical_data