# coding=utf-8
from flask import Blueprint

cobuy = Blueprint('cobuy', __name__)

from . import models, routers
