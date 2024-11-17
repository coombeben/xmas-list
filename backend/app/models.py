from sqlalchemy import func

from .extensions import db


class SerialisableModel:
    def to_dict(self):
        """Utility method to convert object to a dictionary."""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}


class User(db.Model, SerialisableModel):
    user_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    colour = db.Column(db.String(7))


class Item(db.Model, SerialisableModel):
    item_id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), nullable=False)
    name = db.Column(db.String(64), nullable=False)
    description = db.Column(db.Text)
    date_added = db.Column(db.DateTime, nullable=False, server_default=func.now())


class Purchase(db.Model, SerialisableModel):
    user_id = db.Column(db.Integer, db.ForeignKey('user.user_id'), primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('item.item_id'), primary_key=True)
    date = db.Column(db.DateTime, nullable=False, server_default=func.now())


class Session(db.Model):
    token = db.Column(db.String(64), primary_key=True)
    created = db.Column(db.DateTime, nullable=False, server_default=func.now())
