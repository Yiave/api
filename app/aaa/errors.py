from flask import jsonify
from . import aaa


def bad_request(message):
    response = jsonify({'error': 'bad request', 'message': message})
    response.status_code = 400
    return response


def unauthorized(message):
    response = jsonify({'error': 'unauthorized', 'message': message})
    response.status_code = 401
    return response


def forbidden(message):
    response = jsonify({'error': 'forbidden', 'message': message})
    response.status_code = 403
    return response


def notfound(message):
    response = jsonify({'error': 'not found', 'message': message})
    response.status_code = 404
    return response


@aaa.app_errorhandler(405)
def method_not_allowed(e):
    response = jsonify({'error': 'method not allowed', 'message': e.description})
    response.status_code = 405
    return response


def conflict(message):
    response = jsonify({'error': 'already exists', 'message': message})
    response.status_code = 409
    return response


@aaa.app_errorhandler(500)
def internal_server_error(e):
    response = jsonify({'error': 'api server not available', 'message': e.description})
    response.status_code = 500
    return response


@aaa.app_errorhandler(Exception)
def unhandled_exception(e):
    response = jsonify({'error': 'api server not available', 'message': e.message})
    response.status_code = 500
    return response