import app.utils as utils
from .. import db
from datetime import datetime
import hashlib
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from app.basemodel import BaseModel


class Authenticator(BaseModel):
    def authenticate(self):
        pass


class BusinessAuthenticator(Authenticator, db.Model):
    __tablename__ = 'yiave_business_auth_local'

    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer)
    telephone = db.Column(db.String, nullable=True)
    username = db.Column(db.String(100), nullable=True)
    password = db.Column(db.String, nullable=False)

    def update_password(self, password):
        self.password = password
        self.update()

    def to_json(self):
        return {
            "id": self.id,
            "business_id": self.business_id,
            "telephone": self.telephone,
            "username": self.username
        }


class Business(BaseModel, db.Model):
    __tablename__ = 'yiave_business'

    id = db.Column(db.Integer, primary_key=True)
    telephone = db.Column(db.String, nullable=False)
    name = db.Column(db.String(100), nullable=True)
    address = db.Column(db.String(100), nullable=True)
    lon = db.Column(db.Float(7, 3), nullable=True)
    lat = db.Column(db.Float(7, 3), nullable=True)
    hours_open = db.Column(db.Time, nullable=True)
    hours_close = db.Column(db.Time, nullable=True)
    member_level = db.Column(db.Integer, nullable=True)
    member_due_time = db.Column(db.DateTime, nullable=True)
    is_locked = db.Column(db.Boolean)

    def __init__(self, *args, **kwargs):
        super(Business, self).__init__(**kwargs)
        if args:
            if len(args) == 1:
                if isinstance(args[0], dict):
                    self.init_with_json(args[0])
        if kwargs:
            for arg in kwargs:
                if isinstance(kwargs[arg], dict):
                    self.init_with_json(kwargs[arg])
                else:
                    print kwargs
                    self.__dict__[arg] = kwargs[arg]

    def init_with_json(self, data):
        if isinstance(data, dict):
            self.telephone = data["telephone"]
            self.name = data["name"]
            self.address = data["address"]
            self.lon = data["lon"]
            self.lat = data["lat"]
            self.hours_open = data["hours_open"]
            self.hours_close = data["hours_close"]
            self.member_level = data["member_level"]
            self.member_due_time = data["member_due_time"]
            self.is_locked = data["is_locked"]

    def to_json(self):
        return {
            "id": self.id,
            "telephone": self.telephone,
            "name": self.name,
            "address": self.address,
            "lon": str(self.lon),
            "lat": str(self.lat),
            "hours_open": str(self.hours_open),
            "hours_close": str(self.hours_close),
            "member_level": self.member_level,
            "member_due_time": str(self.member_due_time),
            "is_locked": self.is_locked
        }

    @staticmethod
    def from_json(data):
        return Business(data)

    def set_locked(self):
        self.is_locked = True
        self.update()
