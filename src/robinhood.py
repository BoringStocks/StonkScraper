import os
from src import historical
import robin_stocks.robinhood as r


class Robinhood:
    isAuthentificated = False

    @staticmethod
    def __login():
        email = os.getenv("RH_EMAIL")
        password = os.getenv("RH_PASSWORD")
        r.login(email, password)

    @classmethod
    def get_historical(cls, ticker, data_range):
        if not cls.isAuthentificated:
            Robinhood.__login()

        interval = "hour"
        span = ""

        if data_range == '5_days':
            span = "week"
        elif data_range == '1_month':
            span = "month"
        elif data_range == '3_months':
            span = "3month"
        elif data_range == '1_year':
            span = "year"
            interval = "day"
        elif data_range == '5_years':
            span = "5year"
            interval = "week"

        response = r.stocks.get_stock_historicals(
            ticker, interval=interval, span=span)

        # TODO: check for None
        historical = []
        for day in response:
            historical.append({
                "date": day["begins_at"],
                "close": day["close_price"]
            })

        return {"historical": historical}

        # There's 2 types of errors
        # 401 Client Error: Unauthorized for url: https://api.robinhood.com/quotes/historicals/?symbols=GME&interval=hour&span=week&bounds=regular
        # 404 Client Error: Not Found for url: https://api.robinhood.com/quotes/historicals/?symbols=ERDFTCHGVJB&interval=hour&span=week&bounds=regular

    @classmethod
    def get_ticker(cls, ticker):
        if not cls.isAuthentificated:
            Robinhood.__login()

        fundamentals = r.get_fundamentals(ticker)
        # TODO: error handling -> empty array

        ticker_data = {}
        ticker_data["current"] = 0

        ticker_data["volume"] = fundamentals[0]["volume"]
        ticker_data["avg_volume"] = fundamentals[0]["average_volume"]

        ticker_data["market_cap"] = fundamentals[0]["market_cap"]
        ticker_data["market_status"] = 0

        # name = r.stocks.get_name_by_symbol(ticker)
        ticker_data["name"] = "no name"

        # no points change

        ticker_data["range"] = {
            # need to talk about this, also no close
            "open": fundamentals[0]["open"],
            "high": fundamentals[0]["high"],
            "low": fundamentals[0]["low"],
            "date": fundamentals[0]["market_date"]
        }

        ticker_data["symbol"] = fundamentals[0]["symbol"]
        ticker_data["timestamp"] = "1:1:1"

        return ticker_data
