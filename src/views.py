from src import app
from flask import render_template, request, send_file
from .scraper import Scraper
import json
from datetime import datetime
import os.path
from os import path


@app.route('/')
def home():
    """Displays the homepage with forms for current or historical data."""

    return "Nothing to see here, try /ticker"


@app.route('/<ticker>')
def get_all(ticker):

    # Detect if json exists, create new json if none found
    try: 
        # Unpack json to parse time
        unpacked_json = open('data.json')
        data = json.load(unpacked_json)

        format = "%d/%m/%y %H:%M:%S"
        old_time = data['timestamp']
        new_time = (datetime.utcnow()).strftime(format)
        time_delta = datetime.strptime(
            new_time, format) - datetime.strptime(old_time, format)

    except:
        # Run if no JSON found
        print('No JSON found, creating new JSON with requested index')
        stock = Scraper(ticker)

        if stock.page_content == False:
            return 'ERROR - invalid stock index'

        new_data = stock.get_all()

        # new
        with open('data.json', 'w') as stock_json:
            json.dump(new_data, stock_json)

        return new_data


    # Return old/new scrape depending on time_delta between scrapes
    if time_delta.total_seconds() > 5:

        # return new current, write new data into json
        print('Returning new scrape')
        stock = Scraper(ticker)

        if stock.page_content == False:
            return 'ERROR - invalid stock index'

        stock.get_all()

        # new
        new_unpacked_json = open('data.json')
        new_data = json.load(new_unpacked_json)

        return new_data

    else:
        # return old current
        print('Returning old scrape')
        return data