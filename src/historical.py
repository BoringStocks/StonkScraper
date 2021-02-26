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
    print('----------Requesting historical data-----------')
    url = f'https://query1.finance.yahoo.com/v7/finance/download/{ticker.upper()}?period1={math.ceil(period_1)}&period2={math.ceil(period_2)}&interval=1d&events=history&includeAdjustedClose=true'
    print(f'Querying: {url}')
    
    data = requests.get(url)
    
    print(f'Server responded: Status Code {data.status_code}')
    historical_data = []

    # Check if request failed
    if not data:
        return False
    
    decoded = data.content.decode('utf-8')
    csv_reader = csv.DictReader(decoded.splitlines(), delimiter=',')

    for line in csv_reader:
        single_data_point = {}
        single_data_point['date'] = line['Date']

        if line['Close'] != 'null':
            single_data_point['close'] = round(float(line['Close']), 2)
            historical_data.append(single_data_point)
        else:
            print('Null value encountered, skipping')
    print('----------Historical data parse complete-----------\n')

    return historical_data

def normalize_data(data, data_range):

    data_points_count = len(data)
    print(f'Stored data points count: {data_points_count}')
    print(f'Requested data points: {data_range}')

    increment = data_points_count // data_range
    remainder = data_points_count % data_range

    print(f'Increment size: {increment}')
    print(f'Remainder: {remainder}')

    normalized_data = []
    i = 0
    k = 0
    while i < data_points_count-increment:
        date1 = data[i]['date']
        i += increment

        close_totals = 0
        for j in range(increment):
            close_totals += data[k]['close']
            k += 1

        date2 = data[k-1]['date']
        mean = round(close_totals / increment, 2)

        data_point = {}
        data_point['date'] = f'{date1} -> {date2}'
        data_point['close'] = mean
        normalized_data.append(data_point)

    return normalized_data