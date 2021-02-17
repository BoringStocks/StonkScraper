import requests
import json
from bs4 import BeautifulSoup as bs
import html5lib
from datetime import datetime, date
import csv


class Scraper:

    def __init__(self, target):
        self.target = target.upper()
        self.dict = {}
        self.scrape_page()


    def scrape_page(self):
        '''Grab page content, store under self.page_content'''

        self.url = f'https://finance.yahoo.com/quote/{self.target}?p={self.target}&.tsrc=fin-srch'
        self.r = requests.get(self.url)
        self.page_content = bs(self.r.content, features='html5lib')

        # Detect scraping errors
        try:
            self.data_table = self.page_content.find("div", attrs={"id": "quote-summary"})

            # If data_table correctly scrapes, parse containers inside
            try:
                self.parse_open = self.data_table.find('td', attrs={'data-test': 'OPEN-value'})
                self.parse_points_close = self.page_content.find('div', attrs={'class' : 'D(ib) Mend(20px)'})
                self.parse_cap = self.data_table.find('td', attrs={'data-test': 'MARKET_CAP-value'})
                self.parse_volume = self.data_table.find('td', attrs={'data-test': 'TD_VOLUME-value'})
                self.parse_avg_volume = self.data_table.find('td', attrs={'data-test': 'AVERAGE_VOLUME_3MONTH-value'})
                self.parse_market_status = self.page_content.find('div', attrs={'id': 'quote-market-notice'})
                print('Scrape successful\n')

            except:
                self.page_content = False
                print('Error parsing table')
        
        except:
            self.page_content = False
            print('Error fetching table')


    def get_symbol(self):
        '''Return stock symbol'''

        return self.target


    def get_name(self):
        '''Parse self.page_content for stock name, return self.stock_name'''

        self.stock_name = self.page_content.find('h1', attrs={'data-reactid': '7'}).string
        split_data = (self.stock_name).split(' (')
        name = split_data[0]
        return name


    def get_market_status(self):
        '''Return market status:
            1: Open
            0: Closed
        '''

        raw_market_status = (self.parse_market_status.find('span')).string

        if 'open' in raw_market_status:
            return 1
        elif 'close' in raw_market_status:
            return 0

        
    def get_time(self):
        '''Return self.scrape_time'''

        self.scrape_time = (datetime.utcnow()).strftime("%H:%M:%S")
        return self.scrape_time


    def get_open(self):
        '''Parse self.parse_open for open price, return self.open'''

        self.open = float(((self.parse_open.find('span')).string).replace(',',''))
        return self.open

    
    def get_points_change(self):
        '''Parse self.parse_points_close (this is a list, close is index 1) for previous close, return self.points_change'''

        self.points_change = (self.parse_points_close.contents[1]).string

        # Split parsed string into list, i0 = points, i1 = percent
        split_data = (self.points_change).split('(')

        points = split_data[0]

        # Remove paranthese and % from percent string
        percent = split_data[1].replace('%)', '')

        # Store points and percent in dict
        self.points_percent = {}
        self.points_percent['points'] = float(points)
        self.points_percent['percent'] = float(percent)

        return self.points_percent


    def get_current(self):
        '''Parse self.parse_points_close (this is a list, current price is index 0) for previous close, return self.current'''

        self.current = float(((self.parse_points_close.contents[0]).string).replace(',',''))
        return self.current


    def get_cap(self):
        '''Parse self.parse_cap for market cap, return self.cap'''

        self.cap = (self.parse_cap.contents[0]).string
        return self.cap

    
    def get_volume(self):
        '''Parse self.parse_volume for volume, return self.volume'''

        self.volume = float(((self.parse_volume.find('span')).string).replace(',',''))
        return self.volume

    
    def get_avg_volume(self):
        '''Parse self.parse_avg_volume for average volume, return self.avg_volume'''

        self.avg_volume = float(((self.parse_avg_volume.find('span')).string).replace(',',''))
        return self.avg_volume

    
    def get_range(self):
        '''Return high, low, close of index'''
        
        file = requests.get(f"https://query1.finance.yahoo.com/v7/finance/download/{self.target}")
        decoded = file.content.decode('utf-8')
        csv_reader = csv.reader(decoded.splitlines(), delimiter=',')

        data_range = {}
        data_list = list(csv_reader)

        data_range['high'] = round(float(data_list[1][2]), 2)
        data_range['low'] = round(float(data_list[1][3]), 2)
        data_range['close'] = round(float(data_list[1][4]), 2)
        data_range['date'] = data_list[1][0]
        return data_range


    def get_all(self):
        '''Create and call all parse methods on Scraper object'''

        self.dict['avg_volume'] = self.get_avg_volume()
        self.dict['current'] = self.get_current()
        self.dict['market_cap'] = self.get_cap()
        self.dict['market_status'] = self.get_market_status()
        self.dict['name'] = self.get_name()
        self.dict['open'] = self.get_open()
        self.dict['points_change'] = self.get_points_change()
        self.dict['range'] = self.get_range()
        self.dict['symbol'] = self.get_symbol()
        self.dict['timestamp'] = self.get_time()
        self.dict['volume'] = self.get_volume()

        with open('data.json', 'w') as stock_json:
            json.dump(self.dict, stock_json)

        return self.dict