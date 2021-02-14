from src import app
from flask import render_template, request, send_file
from .scraper import Scraper
import json
from datetime import datetime


@app.route('/')
def home():
    """Displays the homepage with forms for current or historical data."""

    return "Nothing to see here, try /ticker"


@app.route('/<ticker>')
def get_all(ticker):

    # Unpack json to parse time
    unpacked_json = open('data.json')
    data = json.load(unpacked_json)

    format = "%H:%M:%S"
    old_time = data['timestamp']
    new_time = (datetime.utcnow()).strftime(format)
    time_delta = datetime.strptime(
        new_time, format) - datetime.strptime(old_time, format)

    # Return old/new scrape depending on time_delta between scrapes
    if time_delta.total_seconds() > 5:

        # return new current, write new data into json
        print('Returning new scrape')
        stock = Scraper(ticker)
        stock.scrape_page()

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


@app.route('/<ticker>/name')
def get_name(ticker):
    stock = Scraper(ticker)
    stock.scrape_page()

    if stock.page_content == False:
        return 'ERROR'

    return stock.get_one('name')