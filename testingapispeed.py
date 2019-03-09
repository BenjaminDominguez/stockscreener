import requests
import urllib.request
import imptime
from apihandler import IEXHandler

"""
Timing the IEXHandler Methods
"""
def get_average_time(func, *args, **kwargs):
    count = 0
    results = []
    while count < 10:
        start = time.time()
        func(*args, **kwargs)
        end = time.time()
        result = end - start
        results.append(result)
        count += 1
    return sum(results)/len(results)


ticker = 'AAPL'
handler = IEXHandler()
func, args = handler.get_current_price, 'AAPL'
print(get_average_time(func, args))

"""
0.5534 seconds on average
"""
func = handler.get_last_x_minute_data
kwargs = {'ticker': 'AAPL', 'minutes': 60}
print(get_average_time(func, **kwargs))

"""
0.579 seconds on average
"""
