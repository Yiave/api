# coding=utf-8
from app import db


class BaseModel():
    def add(self, resource):
        if resource is not None:
            db.session.add(resource)
            return db.session.commit()

    def update(self):
        return db.session.commit()

    def delete(self, resource):
        if resource is not None:
            db.session.delete(resource)
            return db.session.commit()


if __name__ == '__main__':
    pass
