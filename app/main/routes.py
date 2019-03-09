from app.main import bp
from flask import render_template
from flask_login import current_user
from apihandler import IEXHandler

@bp.route('/')
def index():
    watchlist = ['AAPL', 'GOOG']
    handler = IEXHandler()
    # market_idx = ['DJI', 'SPY', 'NDAQ']
    # datasets = [handler.get_last_x_minute_data(idx, 60) for idx in market_idx]
    data = {
    'watchlist': watchlist
    }

    return render_template('main/logged_in_index.html', **data)
