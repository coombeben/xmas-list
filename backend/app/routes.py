from sqlalchemy import func

from .extensions import db


class User(db.Model):
    user_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)


class Item(db.Model):
    item_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    name = db.Column(db.String(64), unique=True, nullable=False)
    description = db.Column(db.Text)
    date_added = db.Column(db.DateTime, server_default=func.now())


class Purchase(db.Model):
    purchase_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('item.item_id'), nullable=False)
    date = db.Column(db.DateTime, server_default=func.now())
