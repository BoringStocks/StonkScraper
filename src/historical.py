from dateutil.relativedelta import relativedelta
import csv
import math
from datetime import datetime
import requests

def retrieve_historical(ticker, data_range):

    if data_range == '5_days':
        period_1 = (datetime.now() - relativedelta(days=7)).timestamp()
    elif data_range == '1_month':
        period_1 = (datetime.now() - relativedelta(months=1)).timestamp()
    elif data_range == '6_months':
        period_1 = (datetime.now() - relativedelta(months=6)).timestamp()
    elif data_range == '1_year':
        period_1 = (datetime.now() - relativedelta(years=1)).timestamp()
    elif data_range == 'max':
        period_1 = 0
    
    period_2 = (datetime.now()).timestamp()
    data = requests.get(
        f'https://query1.finance.yahoo.com/v7/finance/download/{ticker.upper()}?period1={math.ceil(period_1)}&period2={math.ceil(period_2)}&interval=1d&events=history&includeAdjustedClose=true')
    
    historical_data = []
    historical_dict = {}

    # Check if request failed
    if not data:
        return False
    
    decoded = data.content.decode('utf-8')
    csv_reader = csv.DictReader(decoded.splitlines(), delimiter=',')

    for line in csv_reader:
        single_data_point = {}
        single_data_point['date'] = line['Date']
        single_data_point['close'] = round(float(line['Close']), 2)
        historical_data.append(single_data_point)

    historical_dict['historical'] = historical_data
    return historical_dict