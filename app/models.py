from datetime import datetime
from . import db


class BaseModel():
    @classmethod
    def add(self, resource):
        db.session.add(resource)
        return db.session.commit()

    @classmethod
    def update(self):
        return db.session.commit()

    @classmethod
    def delete(self, resource):
        db.session.delete(resource)
        return db.session.commit()

class Authenticator(BaseModel):
    def authenticate(self):
        pass 

class BusinessAuthenticator(Authenticator, db.Model):
    __tablename__ = 'yiave_business_auth_local'

    id = db.Column(db.Integer, primary_key = True)
    business_id = db.Column(db.Integer)
    telephone = db.Column(db.String, nullable = True)
    username = db.Column(db.String(100), nullable = True)
    password = db.Column(db.String, nullable = False)
    
    def setPassword(self, password):
        self.password = password 
    
    def toJson(self):
        return {
            "id": self.id,
            "business_id": self.business_id,
            "telephone": self.telephone,
            "username": self.username,
            "password": self.password
        }

class Promotion(BaseModel, db.Model):
    __tablename__ = 'yiave_promotion'

    id = db.Column(db.Integer, primary_key = True)
    business_id = db.Column(db.Integer)
    title = db.Column(db.String(45), nullable = False)
    image = db.Column(db.String(255))
    description = db.Column(db.String(300), nullable = False)
    publish_date = db.Column(db.DateTime, nullable = True)
    start_time = db.Column(db.DateTime, nullable = False)
    end_time = db.Column(db.DateTime, nullable = False)

    def __init__(self, *args, **kwargs):
        super(Promotion, self).__init__(**kwargs)
        if args:
            if len(args) == 1:
                if isinstance(args[0], dict):
                    self.updateWithJson(args[0])
        if kwargs:
            for arg in kwargs:
                if isinstance(kwargs[arg], dict):
                    self.updateWithJson(kwargs[arg]) #TODO need to reorganize
                else:
                    self.__dict__[arg] = kwargs[arg]

    def updateWithJson(self, prom):
        data = prom 
        if isinstance(data, dict):
            self.business_id = data["business_id"]
            self.title = data["title"]
            self.image = data["image"]
            self.description = data["description"]
            if data.has_key("publish_date"):
                self.publish_date = data["publish_date"]
            self.start_time = data["start_time"]
            self.end_time = data["end_time"]

    def toJson(self):
        return {
            "id": self.id,
            "business_id": self.business_id,
            "title": self.title,
            "image": self.image,
            "description": self.description,
            "start_time": self.start_time,
            "end_time": self.end_time
        }

    @staticmethod 
    def fromJson(data):
        return Promotion(data)
    
    def setDescription(self, desc):
        self.description = desc 

    #def setLock(self, lock):
    #    self.is_locked = lock

class Business(BaseModel, db.Model):
    __tablename__ = 'yiave_business'

    id = db.Column(db.Integer, primary_key = True)
    telephone = db.Column(db.String, nullable = True)
    name = db.Column(db.String(100), nullable = True)
    address = db.Column(db.String(100), nullable = True)
    lon = db.Column(db.Float(7, 3), nullable = True)
    lat = db.Column(db.Float(7, 3), nullable = True)
    hours_open = db.Column(db.Time, nullable = True)
    hours_close = db.Column(db.Time, nullable = True)
    member_level = db.Column(db.Integer, nullable = True)
    member_due_time = db.Column(db.DateTime, nullable = True)
    is_locked = db.Column(db.Boolean)

    def __init__(self, *args, **kwargs):
        super(Business, self).__init__(**kwargs)
        if args:
            if len(args) == 1:
                if isinstance(args[0], dict):
                    self.updateWithJson(args[0])
        if kwargs:
            for arg in kwargs:
                if isinstance(kwargs[arg], dict):
                    self.updateWithJson(kwargs[arg]) #TODO need to reorganize
                else:
                    print kwargs
                    print self 
                    print dir(self)
                    print arg
                    self.__dict__[arg] = kwargs[arg]

    def updateWithJson(self, prom):
        data = prom 
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

    def toJson(self):
        return {
            "telephone" : self.telephone,
            "name" : self.name,
            "address" : self.address,
            "lon" : str(self.lon),
            "lat" : str(self.lat),
            "hours_open" : str(self.hours_open),
            "hours_close" : str(self.hours_close),
            "menber_level" : self.member_level,
            "menber_due_time" : self.member_due_time,
            "is_locked" : self.is_locked
        }

    @staticmethod 
    def fromJson(data):
        return Business(data)
            

    def setLock(self, lock):
        self.is_locked = lock
