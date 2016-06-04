# coding=utf-8

from .models import Business, BusinessAuthenticator
from . import business
from flask import request, current_app, url_for, jsonify, json
from flask import Response
from ..aaa import errors
import app.utils as utils


@business.route('/businesses', methods=['GET'])
def get_businesses():
    page = request.args.get('page', 1, type=int)

    pagination = Business.query.paginate(
        page, per_page=current_app.config['YIAVE_BUSINESSES_PER_PAGE'],
        error_out=False
    )
    businesses = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_businesses', page=page - 1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_businesses', page=page + 1, _external=True)

    data = [b.to_json() for b in businesses]
    response = Response(json.dumps(data))
    response.headers['Content-Type'] = "application/json"
    response.headers['X-Page-Pre'] = prev
    response.headers['X-Page-Next'] = next
    response.headers['X-Total-Count'] = pagination.total
    return response


@business.route('/businesses/<int:id>', methods=['GET'])
def get_business(id):
    business = Business.query.get(id)
    if not business:
        return errors.notfound("Business not found")
    return jsonify(business.to_json())  # string to json


@business.route('/businesses/telephone/<string:tel>', methods=['GET'])
def get_business_by_telephone(tel):
    business = Business.query.filter_by(telephone=tel).first()
    if not business:
        return errors.notfound("telephone not exist")

    return jsonify(business.to_json())


@business.route('/businesses/<int:id>/password', methods=['PUT', 'PATCH'])
def update_password(id):
    business = BusinessAuthenticator.query.get(id)
    if not business:
        return errors.notfound("Business not found")
    new_password = request.json['password']
    business.update_password(new_password)
    return jsonify(business.to_json())


@business.route('/businesses/<int:id>', methods=['DELETE'])
def delete_business(id):
    business = Business.query.get(id)
    if not business:
        return errors.notfound("Business not found")
    business.set_locked()
    return jsonify(business.to_json())


if __name__ == '__main__':
    pass
