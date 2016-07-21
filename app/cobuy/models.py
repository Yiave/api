# coding=utf-8
import app.utils as utils
from .. import db
from datetime import datetime
import hashlib
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from app.basemodel import BaseModel


class Wish(BaseModel, db.Model):
    __tablename__ = 'yiave_wish'
    id = db.Column(db.Integer, primary_key=True)
    promotion_id = db.Column(db.Integer)
    customer_id = db.Column(db.Integer)
    wish_count = db.Column(db.Integer)
    wish_time_start = db.Column(db.DateTime)
    wish_time_end = db.Column(db.DateTime)
    match_type = db.Column(db.Integer)
    is_matched = db.Column(db.Boolean, default=0)
    is_open = db.Column(db.Boolean, default=1)

    def __init__(self, *args, **kwargs):
        super(Wish, self).__init__(**kwargs)

        if args:  # position args
            if len(args) == 1:  # only one data passed
                if isinstance(args[0], dict):
                    self.init_with_json(args[0])
        if kwargs:  # keywords args
            for arg in kwargs:
                if isinstance(kwargs[arg], dict):
                    self.init_with_json(kwargs[arg])
                else:
                    self.__dict__[arg] = kwargs[arg]

    def init_with_json(self, data):
        if isinstance(data, dict):
            self.customer_id = data['customer_id']
            self.wish_count = data['wish_count']
            self.wish_time_start = data['wish_time_start']
            self.wish_time_end = data['wish_time_end']
        return self

    def to_json(self):
        return {
            "id": self.id,
            "promotion_id": self.promotion_id,
            "customer_id": self.customer_id,
            "wish_count": self.wish_count,
            "wish_time_start": str(self.wish_time_start),
            "wish_time_end": str(self.wish_time_end),
            "match_type": self.match_type,
            "is_matched": self.is_matched,
            "is_open": self.is_open
        }

    @staticmethod
    def from_json(data):
        return Wish(data)

    def update_open(self, is_open):
        self.is_open = is_open
        self.update()


class Cobuy(BaseModel, db.Model):
    __tablename__ = 'yiave_cobuy'
    id = db.Column(db.Integer, primary_key=True)
    wish_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer)
    promotion_id = db.Column(db.Integer)
    promotion_count = db.Column(db.Integer)
    match_type = db.Column(db.Integer)
    end_time = db.Column(db.DateTime)
    is_match_completed = db.Column(db.Boolean, default=0)
    min_time = db.Column(db.DateTime)
    max_time = db.Column(db.DateTime)


    def __init__(self, *args, **kwargs):
        super(Cobuy, self).__init__(**kwargs)

        if args:  # position args
            if len(args) == 1:  # only one data passed
                if isinstance(args[0], dict):
                    self.init_with_json(args[0])
        if kwargs:  # keywords args
            for arg in kwargs:
                if isinstance(kwargs[arg], dict):
                    self.init_with_json(kwargs[arg])
                else:
                    self.__dict__[arg] = kwargs[arg]

    def init_with_json(self, data):
        if isinstance(data, dict):
            self.match_type = data['match_type']
        return self

    def to_json(self):
        return {
            "id": self.id,
            "wish_id": self.wish_id,
            "promotion_id": self.promotion_id,
            "promotion_count": self.promotion_count,
            "customer_id": self.customer_id,
            "match_type": self.match_type,
            "end_time": str(self.end_time),
            "is_match_completed": self.is_match_completed,
            "min_time": str(self.min_time),
            "max_time": str(self.max_time)
        }


if __name__ == '__main__':
    pass
