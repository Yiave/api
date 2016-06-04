# coding=utf-8
import app.utils as utils
from .. import db
from datetime import datetime
import hashlib
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from app.basemodel import BaseModel

class Cobuy(BaseModel, db.Model):
    __tablename__ = 'yiave_cobuy'
    id = db.Column(db.Integer, primary_key = True)
    wish_id = db.Column(db.Integer)
    customer_id = db.Column(db.Integer)
    promotion_id = db.Column(db.Integer)
    match_type = db.Column(db.Boolean)
    end_time = db.Column(db.DateTime)
    is_match_completed = db.Column(db.Boolean)

class Wish(BaseModel, db.Model):
    __tablename__ = 'yiave_wish'
    id = db.Column(db.Integer, primary_key = True)
    promotion_id = db.Column(db.Integer)
    customer_id = db.Column(db.Integer)
    wish_count = db.Column(db.Integer)
    wish_time_start = db.Column(db.DateTime)
    wish_time_end = db.Column(db.DateTime)
    match_type = db.Column(db.Boolean)
    is_matched = db.Column(db.Boolean)
if __name__ == '__main__':
    pass
