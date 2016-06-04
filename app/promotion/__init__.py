# coding=utf-8
from flask import Blueprint

promotion = Blueprint('promotion', __name__)

from . import models,routers