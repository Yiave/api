# coding=utf-8
from flask import Blueprint

customer = Blueprint('customer', __name__)

from . import models, routers