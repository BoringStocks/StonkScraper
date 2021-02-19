from src import app
from flask import request, jsonify
from flask_api import status
from .scraper import Scraper
from .historical import retrieve_historical
import json
from datetime import datetime


@app.route('/v1/')
def home():
    """Displays the homepage with forms for current or historical data."""

    return "Nothing to see here, try /ticker"


@app.route('/v1/<ticker>')
def get_all(ticker):
    print(f'{ticker} requested at {datetime.utcnow()}')

    # Detect if json exists, create new json if none found
    try:
        # Unpack old json to parse time
        with open('data.json', 'r') as data_json:
            old_json = json.load(data_json)

        # Determine difference between old/new timestamps
        format = "%H:%M:%S"
        old_time = old_json['timestamp']
        new_time = (datetime.utcnow()).strftime(format)
        time_delta = datetime.strptime(
            new_time, format) - datetime.strptime(old_time, format)

        # Return new scrape if difference in stamps exceeds 5 secs or new index is requested
        if abs(time_delta.total_seconds()) >= 5 or old_json['symbol'] != ticker.upper():

            # return new current, write new data into json
            print('Returning new scrape')
            stock = Scraper(ticker)

            if not stock.page_content:
                return f'{ticker} not found', status.HTTP_400_BAD_REQUEST

            data = stock.get_all()

            # Call 5_day historical
            historical = retrieve_historical(ticker, '5_days')

            data['historical'] = historical

            # Write payload to json
            with open('data.json', 'w') as data_json:
                json.dump(data, data_json)

            return data

        else:
            # return old data if timestamp difference less than 5 secs
            print('Returning old scrape')
            return old_json

    except:
        # Run if no JSON found
        print('No JSON found, creating new JSON with requested index')
        stock = Scraper(ticker)

        if not stock.page_content:
            return f'{ticker} not found', status.HTTP_400_BAD_REQUEST

        # Retrieve scrape data
        data = stock.get_all()

        # Call 5_day historical
        historical = retrieve_historical(ticker, '5_days')

        data['historical'] = historical

        # Write scrape to new json
        with open('data.json', 'w') as data_json:
            json.dump(data, data_json)

        return data


@app.route('/v1/<ticker>/historical/<data_range>')
def get_historical(ticker, data_range):
    '''Retrieve historical data spanning a given range in 1 day increments'''

    if data_range == '5_days':
        data = retrieve_historical(ticker, '5_days')
    elif data_range == '1_month':
        data = retrieve_historical(ticker, '1_month')
    elif data_range == '6_months':
        data = retrieve_historical(ticker, '6_months')
    elif data_range == '1_year':
        data = retrieve_historical(ticker, '1_year')
    elif data_range == 'max':
        data = retrieve_historical(ticker, 'max')
    else:
        return f'{data_range} invalid. Try 5_days, 1_month, 6_months, 1_year, max', status.HTTP_400_BAD_REQUEST

    if not data:
        return f'{ticker} not found', status.HTTP_400_BAD_REQUEST

    return jsonify(data)