from app.stock import bp
from app.models import StockModel
from iexfinance.stocks import Stock, get_historical_intraday
from flask import abort, flash, render_template, current_app, session
import requests
import json
import pandas as pd
from app import db
from datetime import datetime
from app.special import buttons, minute_data
from apihandler import IEXHandler, jsonminute
import time

@bp.route('/stock/<ticker>')
def stock(ticker):
    # start = time.time()
    # """
    # Four sources of information,
    # (1) A pandas dataframe with the intraday stock information (Useful for daily graphs)
    # (2) A iexfinance.stocks.Stock instance
    # (3) A pandas dataframe with yearly and daily information
    # (4) SQLAlchemy models instance of the ticker, if the ticker does not return a key error from IEX, create it in the database.
    # """
    # iex = IEXHandler()
    #
    # price = iex.get_current_price(ticker)
    # ticker_price_var = '{0}_price'.format(ticker)
    #
    # session[ticker_price_var] = price
    #
    # data15 = jsonminute(iex.get_last_x_minute_data, ticker, minutes=15)
    # data60 = jsonminute(iex.get_last_x_minute_data, ticker, minutes=60)
    # datatoday = jsonminute(iex.get_last_x_minute_data, ticker)
    # daily_return = round(iex.get_yesterdays_close_price(ticker)[1], 2)
    # ticker_change_var = '{0}_change'.format(ticker)
    #
    # session[ticker_change_var] = daily_return
    # end = time.time()
    # time_elapsed = round((end - start), 2)
    # flash("{0} seconds taken".format(time_elapsed))
    # kwargs = {
    # 'ticker': ticker, 'price': price, 'data15': data15, 'data60': data60, 'datatoday': datatoday,
    # 'sp_active': True, 'daily_return': round(daily_return, 2)
    # }

    kwargs = {'ticker': ticker}
    return render_template('stock/stock_price.html', **kwargs)

@bp.route('/stock/<ticker>/bs')
def bs(ticker):
    return render_template('stock/bs.html', ticker=ticker, bs_active=True)

@bp.route('/stock/<ticker>/is')
def income_st(ticker):
    iex = IEXHandler()
    return render_template('stock/is.html', ticker=ticker, is_active=True)

@bp.route('/stock/<ticker>/fr')
def fr(ticker):
    return render_template('stock/fr.html', ticker=ticker, fr_active=True)

@bp.route('/stock/<ticker>/kf')
def kf(ticker):
    return render_template('stock/kf.html', ticker=ticker,kf_active=True)
