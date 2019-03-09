"""
Write a script that web scrapes for financial data for each stock in my database
"""

import requests
from bs4 import BeautifulSoup

class YahooFinanceScraper(object):

    base_url = 'https://finance.yahoo.com/quote/{0}/key-statistics?p={0}'

    def __init__(self, ticker):
        self.ticker = ticker
        self.url = requests.get(self.base_url.format(ticker)).text
        self.soup = BeautifulSoup(self.url, 'html.parser')

    def get_valuation_measures(self):
        tables = self.soup.find('table', {'class': 'table-qsp-stats'})
        tds = [td.text.strip() for td in tables.findAll('td')]
        keys = ['Market Cap',
        'Enterprise Value',
        'Trailing PE',
        'Forward PE',
        'PEG Ratio',
        'Price/Sales',
        'Price/Book',
        'EV/Revenue'
        'EV/EBIDTA'
        ]
        values = [tds[i] for i in range(len(tds)) if i % 2 != 0]
        data = dict(zip(keys, values))
        return data
