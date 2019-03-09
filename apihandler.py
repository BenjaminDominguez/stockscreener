import requests, json
from iexfinance.stocks import get_historical_intraday
from datetime import datetime, timedelta
import os

class DataModel(object):
    def __init__(self, name, BASE_URL, SECRET_KEY, PUBLIC_KEY):
        self.name = name
        self.BASE_URL = BASE_URL
        self.SECRET_KEY = SECRET_KEY

    def get_current_price(self):
        pass

    def get_yesterdays_close_price(self):
        pass

    def get_last_x_minute_data(self):
        pass

    def get_income_statement(self):
        pass


class IEXHandler(DataModel):
    def __init__(self):
        data = {
        'name': 'IEX',
        'BASE_URL': 'https://cloud.iexapis.com',
        'SECRET_KEY': os.environ.get('IEX_SECRET_KEY'),
        'PUBLIC_KEY': os.environ.get('IEX_PUBLIC_KEY')
        }
        DataModel.__init__(self, **data)
        self.VERSION = 'beta'

    def get_current_price(self, ticker):
        url = "{0}/{1}/{2}".format(self.BASE_URL, self.VERSION, 'tops')
        params = {'token': self.SECRET_KEY, 'symbols': ticker}
        r = requests.get(url, params=params)
        try:
            return r.json()[0]['lastSalePrice']
        except IndexError:
            return 175

    def get_yesterdays_close_price(self, ticker):
        url = "{0}/{1}/stock/{2}/previous".format(self.BASE_URL, self.VERSION, ticker)
        params = {'token': self.SECRET_KEY}
        r = requests.get(url, params=params)

        yesterday = r.json()['close']
        today = self.get_current_price(ticker)
        change = (yesterday/today) - 1
        """
        Returns yesterday's close price, along with the percent change
        from yesterday to the current price
        """
        return (yesterday, change*100)

    def get_last_x_minute_data(self, ticker, minutes=0):
        today = datetime.today()
        yesterday = today - timedelta(1)
        try:
            df = get_historical_intraday(ticker, today, output_format='pandas')['close']
        except KeyError:
            df = get_historical_intraday(ticker, yesterday, output_format='pandas')['close']
        if minutes:
            return list(df.head(minutes))
        else:
            return list(df)

    def get_income_statement(self, ticker, period='annual'):
        url = "{0}/{1}/stock/{2}/income".format(self.BASE_URL, self.VERSION, ticker)
        params = {'token': self.SECRET_KEY, 'period': period}
        r = requests.get(url, params=params)
        """
        output is

        {'reportDate': '2018-09-30',
        'totalRevenue': 265809000000,
        'costOfRevenue': 163826000000,
        'grossProfit': 101983000000,
        'researchAndDevelopment': 14236000000,
        'sellingGeneralAndAdmin': 16705000000,
        'operatingExpense': 194767000000,
        'operatingIncome': 71042000000,
        'otherIncomeExpenseNet': 1861000000,
        'ebit': 71042000000,
        'interestIncome': 3240000000,
        'pretaxIncome': 72903000000,
        'incomeTax': 13372000000,
        'minorityInterest': 0,
        'netIncome': 59531000000,
        'netIncomeBasic': 59531000000
        }

        """
        return r.json()['income'][0]

class WebScraperHandler(DataModel):

    pass

def jsonminute(func, ticker, minutes=0):
    data = func(ticker, minutes)
    return {
    'type': 'line',
    'data': {
    'labels': list(range(len(data) + 1)),
    'datasets': [
    {'label': '{0} stock price'.format(ticker.upper()),
    'data': data,
    'fill': True,
    'borderColor': 'rgb(100, 192, 192)',
    'backgroundColor': 'rgb(100, 192, 192)',
    'lineTension': 0.1}
    ],
    'options': {'responsive': 'true'}}
    }
