# coding=utf-8

from flask import Blueprint

aaa = Blueprint("aaa", __name__)

from . import customers, errors
