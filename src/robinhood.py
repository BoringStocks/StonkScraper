import robin_stocks.robinhood as r


class Robinhood:
    isAuthentificated = False

    @staticmethod
    def __login():
        r.login()

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
        historical_data = []
        for day in response:
            historical_data.append({
                "date": day["begins_at"],
                "close": day["close_price"]
            })

        return historical_data

        # There's 2 types of errors
        # 401 Client Error: Unauthorized for url: https://api.robinhood.com/quotes/historicals/?symbols=GME&interval=hour&span=week&bounds=regular
        # 404 Client Error: Not Found for url: https://api.robinhood.com/quotes/historicals/?symbols=ERDFTCHGVJB&interval=hour&span=week&bounds=regular


# print(ticker)
# name = r.stocks.get_name_by_symbol(ticker)
# fundamentals = r.stocks.get_fundamentals(ticker)

# data = {}
# data["ticker"] = ticker
# data["name"] = name
# data["fundamentals"] = fundamentals
# return data
