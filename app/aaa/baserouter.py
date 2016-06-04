# coding=utf-8
from flask import jsonify, request, current_app, url_for, Response, json
import app.utils as utils
from .errors import bad_request, unauthorized, forbidden, notfound, conflict
from . import aaa


@aaa.before_app_request
def before_request():
    if request.method != "OPTIONS":
        if not request.headers.get("Authorization"):
            return unauthorized("Unauthorized API")


@aaa.after_app_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, PUT, PATCH, DELETE, OPTIONS")
    response.headers.add('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Content-Type', 'application/json')
    return response


if __name__ == '__main__':
    pass
