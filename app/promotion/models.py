# coding=utf-8
import app.utils as utils
from .. import db
from datetime import datetime
import hashlib
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from app.basemodel import BaseModel


class Promotion(BaseModel, db.Model):
    __tablename__ = 'yiave_promotion'

    id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer)
    title = db.Column(db.String(45), nullable=False)
    image = db.Column(db.String(255))
    promotion_count = db.Column(db.Integer)
    type = db.Column(db.Integer)
    description = db.Column(db.String(300), nullable=False)
    publish_date = db.Column(db.DateTime, nullable=True)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)

    def __init__(self, *args, **kwargs):
        super(Promotion, self).__init__(**kwargs)
        if args:
            if len(args) == 1:
                if isinstance(args[0], dict):
                    self.init_with_json(args[0])
        if kwargs:
            for arg in kwargs:
                if isinstance(kwargs[arg], dict):
                    self.init_with_json(kwargs[arg])
                else:
                    self.__dict__[arg] = kwargs[arg]

    def init_with_json(self, data):
        if isinstance(data, dict):
            self.business_id = data["business_id"]
            self.title = data["title"]
            self.image = data["image"]
            self.description = data["description"]
            self.type = data["type"]
            self.promotion_count = data["promotion_count"]
            self.publish_date = utils.get_datetime()
            self.start_time = data["start_time"]
            self.end_time = data["end_time"]

    def to_json(self):
        return {
            "id": self.id,
            "business_id": self.business_id,
            "title": self.title,
            "image": self.image,
            "type": self.type,
            "promotion_count": self.promotion_count,
            "description": self.description,
            "start_time": str(self.start_time),
            "end_time": str(self.end_time),
            "publish_date": str(self.publish_date)
        }

    @staticmethod
    def from_json(data):
        return Promotion(data)


class PromotionClothingcount(BaseModel, db.Model):
    __tablename__ = 'yiave_promotion_clothingcount'

    id = db.Column(db.Integer, primary_key=True)
    promotion_id = db.Column(db.Integer)
    clothing_count = db.Column(db.Integer)
    discount = db.Column(db.Float)

    def __init__(self, *args, **kwargs):
        super(PromotionClothingcount, self).__init__(**kwargs)


class PromotionConsumecount(BaseModel, db.Model):
    __tablename__ = 'yiave_promotion_consumecount'

    id = db.Column(db.Integer, primary_key=True)
    promotion_id = db.Column(db.Integer)
    consume_count = db.Column(db.Integer)
    discount = db.Column(db.Integer)

    def __init__(self, *args, **kwargs):
        super(PromotionConsumecount, self).__init__(**kwargs)


if __name__ == '__main__':
    pass
