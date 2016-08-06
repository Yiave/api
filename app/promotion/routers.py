# coding=utf-8
from .models import Promotion
from . import promotion
from flask import request, current_app, url_for, jsonify, json
from flask import Response
from flask import Flask, make_response
from functools import wraps
import flask
from flask import render_template, redirect
from ..aaa import errors


@promotion.route('/promotions', methods=['GET'])
def get_promotions():
    page = request.args.get('page', 1, type=int)

    pagination = Promotion.query.paginate(
        page, per_page=current_app.config['YIAVE_PROMOTIONS_PER_PAGE'],
        error_out=False
    )
    promotions = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_promotions', page=page - 1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('api.get_promotions', page=page + 1, _external=True)

    data = [p.to_json() for p in promotions]
    response = Response(json.dumps(data))
    response.headers['Content-Type'] = "application/json"
    response.headers['X-Page-Pre'] = prev
    response.headers['X-Page-Next'] = next
    response.headers['X-Total-Count'] = pagination.total
    return response


@promotion.route('/promotions/<int:id>', methods=['GET'])
def get_promotion(id):
    promotion = Promotion.query.get(id)
    if not promotion:
        return errors.notfound("Promotion not found")
    return jsonify(promotion.to_json())

@promotion.route('/promotions/business/<int:id>', methods=['GET'])
def get_promotions_by_business(id):
    promotions = Promotion.query.filter(Promotion.business_id == id).all()
    if not promotions:
        return errors.notfound("Promotion for Business " + str(id) + " not found")
    return json.dumps([p.to_json() for p in promotions])

@promotion.route('/promotions', methods=['POST'])
def create_promotion():
    data = request.json
    promotion = Promotion.from_json(data)
    promotion.add(promotion)
    return jsonify(promotion.to_json())


@promotion.route('/promotions/<int:id>', methods=['PUT', 'PATCH'])
def update_promotion(id):
    promotion = Promotion.query.get(id)
    if not promotion:
        return errors.notfound("Promotion not found")
    description = request.json['description']
    promotion.description = description
    promotion.update()
    return jsonify(promotion.to_json())


if __name__ == '__main__':
    pass
