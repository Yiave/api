from datetime import datetime
import hashlib
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from app import db
from app.basemodel import BaseModel
import app.utils as utils


class Authenticator(BaseModel):
    def authenticate(self):
        pass


class LocalAuthenticator(Authenticator, db.Model):
    __tablename__ = 'yiave_customer_auth_local'

    id = db.Column(db.BigInteger, primary_key=True)
    customer_id = db.Column(db.Integer)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String, nullable=False, unique=True)
    telephone = db.Column(db.String, nullable=True, unique=True)
    password = db.Column(db.String, nullable=False)

    def authenticate(self):
        pass


class OauthAuthenticator(Authenticator, db.Model):
    __tablename__ = 'yiave_customer_auth_oauth'

    id = db.Column(db.BigInteger, primary_key=True)
    customer_id = db.Column(db.Integer)
    oauth_name = db.Column(db.String)
    oauth_id = db.Column(db.String)
    oauth_access_token = db.Column(db.String)
    oauth_expires = db.Column(db.Integer)

    def authenticate(self):
        pass


class Customer(BaseModel, db.Model):
    __tablename__ = 'yiave_customer'

    id = db.Column(db.BigInteger, primary_key=True)
    username = db.Column(db.String, nullable=False, unique=True)
    email = db.Column(db.String(64), nullable=False, unique=True)
    telephone = db.Column(db.String(64), nullable=True, unique=True)
    nickname = db.Column(db.String(64), nullable=True)
    gender = db.Column(db.String(2), nullable=True)
    avater_url = db.Column(db.String(64), nullable=True)
    realname = db.Column(db.String(64), nullable=True)
    signup_date = db.Column(db.String, nullable=True)
    last_signin_date = db.Column(db.String, nullable=True)
    is_confirmed = db.Column(db.Boolean, nullable=True, default=False)
    is_locked = db.Column(db.Boolean, nullable=True, default=False)

    def __init__(self, *args, **kwargs):
        super(Customer, self).__init__(**kwargs)

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
            self.telephone = data['telephone']
            self.email = data['email']
            self.nickname = data['nickname']
        return self

    # Sign Up
    def get_confirm_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'customer_id': self.id})

    def set_confirmed(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('customer_id') != self.id:
            return False
        self.is_confirmed = True
        self.update()
        return True

    def toJSON(self):
        return {
            'id': self.id,
            'username': self.username,
            'telephone': self.telephone,
            'email': self.email,
            'avater_url': self.avater_url,
            'nickname': self.nickname,
            'gender': self.gender,
            'realname': self.realname,
            'signup_date': str(self.signup_date),
            'last_signin_date': str(self.last_signin_date),
            'is_confirmed': self.is_confirmed,
            'is_locked': self.is_locked
        }

    @staticmethod
    def fromJSON(data):
        return Customer(data)

    def set_last_signin_date(self):
        self.last_signin_date = utils.getDatetime()
        self.update()