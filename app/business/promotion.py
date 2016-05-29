from ..models import Promotion 
from . import api
from flask import request, current_app, url_for, jsonify, json
from flask import Response
from flask import Flask, make_response
from functools import wraps
import flask
from flask import render_template, redirect
from . import errors 


@api.before_app_request
def before_request():
    if not request.headers.get("Authorization"):
        return errors.unauthorized("Unauthorized API")

@api.route('/promotions', methods = ['GET'])
def get_promotions():
    page = request.args.get('page', 1, type = int)

    pagination = Promotion.query.paginate(
        page, per_page = current_app.config['YIAVE_PROMOTIONS_PER_PAGE'],
        error_out = False
        )
    promotions = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_promotions', page = page - 1, _external = True)
    next = None 
    if pagination.has_next:
        next = url_for('api.get_promotions', page = page + 1, _external = True)

    data = [p.toJson() for p in promotions]
    response =  Response(json.dumps(data))
    response.headers['Content-Type'] = "application/json"
    response.headers['X-Page-Pre'] = prev
    response.headers['X-Page-Next'] = next 
    response.headers['X-Total-Count'] = pagination.total
    return response


@api.route('/promotions/<int:id>', methods = ['GET'])
def get_promotion(id):
    promotion = Promotion.query.get_or_404(id)
    return jsonify(promotion.toJson()) # string to json 

@api.route('/promotions', methods = ['POST'])
def create_promotion():
   promotionJson = request.json
   Promotion.add(Promotion.fromJson(promotionJson))
   return json.dumps(promotionJson) # object to json  

@api.route('/promotions/<int:id>', methods = ['PUT', 'PATCH'])
def update_promotion(id):
    promotion = Promotion.query.get_or_404(id)
    description = request.json['description']
    promotion.setDescription(description)
    promotion.update()
    return jsonify(promotion.toJson()) 

#@api.route('/promotions/<int:id>', methods = ['DELETE'])
#def deletePromotion(id):
#    promotion = Promotion.query.get_or_404(id)
#    is_locked = request.json['is_locked']
#    promotion.setLock(is_locked)
#    promotion.update()
#    return jsonify(promotion.toJson()) 
