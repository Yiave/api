# coding=utf-8

import re
from datetime import datetime

def getDatetime():
    return datetime.now().strftime("%Y-%m-%d %H:%M;%S")

def isEmail(email):
    if not re.match("[^@]+@[^@]+\.[^@]+", email):
        return False
    return True

if __name__ == '__main__':
    pass