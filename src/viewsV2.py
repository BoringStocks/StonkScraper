from src import app
from .robinhood import Robinhood
import json
from datetime import datetime
import traceback
from flask_api import status

Robinhood.login()

@app.route('/v2/<ticker>')
def get_all_v2(ticker):
    data = Robinhood.get_ticker(ticker)

    if not data:
        return f'{ticker} not found', status.HTTP_400_BAD_REQUEST

    return data


@app.route('/v2/<ticker>/historical/<data_range>')
def get_historical_v2(ticker, data_range):
    historical_data = Robinhood.get_historical(
        ticker, data_range)

    if not historical_data:
        return f'{ticker} not found', status.HTTP_400_BAD_REQUEST

    return historical_data