from src import app, historical
from .robinhood import Robinhood

# https://github.com/jmfernandes/robin_stocks
# http://www.robin-stocks.com/en/latest/robinhood.html#getting-stock-information


@app.route('/v2/<ticker>')
def get_all_v2(ticker):
    ticker_data = Robinhood.get_ticker(ticker)

    # TODO: error handling

    return ticker_data


@app.route('/v2/<ticker>/historical/<data_range>')
def get_historical_v2(ticker, data_range):
    historical_data = Robinhood.get_historical(
        ticker, data_range)

    # TODO: error handling

    return historical_data
