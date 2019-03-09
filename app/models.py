from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), unique=True, index=True)
    #stored as a hash
    password = db.Column(db.String(100))
    watchlist = db.relationship('StockModel', backref='watcher', lazy='dynamic')

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

class StockModel(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ticker = db.Column(db.String(32), unique=True)
    company_name = db.Column(db.String(64))
    exchange = db.Column(db.String(64))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
