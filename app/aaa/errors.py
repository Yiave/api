from flask import jsonify
from app.exceptions import ValidationError
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
    print message
    response = jsonify({'error': 'not found', 'message': message})
    response.status_code = 404
    return response


def conflict(message):
    response = jsonify({'error': 'already exists', 'message': message})
    response.status_code = 409
    return response


@aaa.errorhandler(ValidationError)
def validation_error(e):
    return bad_request(e.args[0])
