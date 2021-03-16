import os
from datetime import datetime, date
import json
import robin_stocks.robinhood as r


class Robinhood:
    isAuthentificated = False
    login_time = ''

    @classmethod
    def login(cls):
        email = os.getenv("RH_EMAIL")
        password = os.getenv("RH_PASSWORD")
        r.login(email, password)
        cls.login_time = (datetime.utcnow()).strftime("%H:%M:%S")
        

    @classmethod
    def get_historical(cls, ticker, data_range):
        format = "%H:%M:%S"
        current_time = (datetime.utcnow()).strftime("%H:%M:%S")

        time_delta = abs(datetime.strptime(cls.login_time, format) - datetime.strptime(current_time, format))

        # Relogin after 22 hours
        if time_delta.total_seconds() >= 79200:
            Robinhood.login()

        interval = ""
        span = ""


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
            print('Bad ticker, responding with error 400')
            return False

        historical = []
        for day in response:
            historical.append({
                "date": day["begins_at"],
                "close": day["close_price"]
            })

        return {"historical": historical}

    @classmethod
    def get_ticker(cls, ticker):
        format = "%H:%M:%S"
        current_time = (datetime.utcnow()).strftime("%H:%M:%S")

        time_delta = abs(datetime.strptime(cls.login_time, format) - datetime.strptime(current_time, format))

        # Relogin after 22 hours
        if time_delta.total_seconds() >= 79200:
            Robinhood.login()

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
            "open": round(float(fundamentals[0]["open"]),2),
            "high": round(float(fundamentals[0]["high"]),2),
            "low": round(float(fundamentals[0]["low"]),2),
            "date": fundamentals[0]["market_date"]
        }

        ticker_data["symbol"] = fundamentals[0]["symbol"]
        ticker_data["timestamp"] = (datetime.utcnow()).strftime("%H:%M:%S")

        return ticker_data