import os
from datetime import datetime, date
import json
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

        interval = ""
        span = ""

# 1 day, 5 days, 3 month, 1 year, 5 years
# 1 day, interval 5minute
# 5 days, interval 1 hour
# 3 month, interval day
# 1 year, interval day
# 5 year, interval week

        if data_range == '1_day':
            span = "day"
            interval = "5minute"
        elif data_range == '5_days':
            span = "week"
            interval = "hour"
        elif data_range == '3_months':
            span = "3month"
            interval = "day"
        elif data_range == '1_year':
            span = "year"
            interval = "day"
        elif data_range == '5_years':
            span = "5year"
            interval = "week"

        response = r.stocks.get_stock_historicals(
            ticker, interval=interval, span=span)
        
        # Check if data doesn't exist
        if response[0] == None:
            return False

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
        if fundamentals[0] == None:
            return False

        ticker_data = {}
        ticker_data["current"] = round(float(r.stocks.get_latest_price(ticker)[0]),2)
        ticker_data["volume"] = round(float(fundamentals[0]["volume"]),2)
        ticker_data["avg_volume"] = round(float(fundamentals[0]["average_volume"]), 2)
        ticker_data["market_cap"] = round(float(fundamentals[0]["market_cap"]), 2)
        ticker_data["market_status"] = 0
        ticker_data["name"] = r.stocks.find_instrument_data(ticker)[0]['simple_name']
        ticker_data['points_change'] = 0
        ticker_data["range"] = {
            # need to talk about this, also no close
            "open": round(float(fundamentals[0]["open"]),2),
            "high": round(float(fundamentals[0]["high"]),2),
            "low": round(float(fundamentals[0]["low"]),2),
            "date": fundamentals[0]["market_date"]
        }

        ticker_data["symbol"] = fundamentals[0]["symbol"]
        ticker_data["timestamp"] = (datetime.utcnow()).strftime("%H:%M:%S")

        with open('data.json', 'w') as stock_json:
            json.dump(ticker_data, stock_json)

        return ticker_data