from iexfinance.stocks import get_historical_intraday
from datetime import datetime, timedelta
"""
Price data functions
"""

def minute_data(minutes, ticker):
    today = datetime.today()
    try:
        df = get_historical_intraday(ticker, today, output_format='pandas')['open']
    except KeyError:
        yesterday = today - timedelta(1)
        df = get_historical_intraday(ticker, yesterday, output_format='pandas')['open']
    return list(df.head(minutes))

buttons = [
{
'name': 'Last 60 minutes',
'id': '60min',
'format': 'minutes',
'value': 60
},
{
'name': 'Last week',
'id': '7d',
'format': 'days',
'value': 7
},{
'name': 'Last month',
'id': '1mo',
'format': 'months',
'value': 1
}
]
