from ..models import Business, BusinessAuthenticator 
from . import api
from flask import request, current_app, url_for, jsonify, json
from flask import Response
from . import errors 
import app.utils as utils

@api.before_app_request
def before_request():
    if not request.headers.get("Authorization"):
        return errors.unauthorized("Unauthorized API")

@api.route('/businesses', methods = ['GET'])
def get_businesses():
    page = request.args.get('page', 1, type = int)

    pagination = Business.query.paginate(
        page, per_page = current_app.config['YIAVE_BUSINESSES_PER_PAGE'],
        error_out = False
        )
    businesses = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('api.get_businesses', page = page - 1, _external = True)
    next = None 
    if pagination.has_next:
        next = url_for('api.get_businesses', page = page + 1, _external = True)

    data = [b.toJson() for b in businesses]
    response =  Response(json.dumps(data))
    response.headers['Content-Type'] = "application/json"
    response.headers['X-Page-Pre'] = prev
    response.headers['X-Page-Next'] = next 
    response.headers['X-Total-Count'] = pagination.total
    return response



@api.route('/businesses/<int:id>', methods = ['GET'])
def get_business(id):
    business = Business.query.get_or_404(id)
    return jsonify(business.toJson()) # string to json 

# generate telephone authcode 
@api.route('/businesses/generate_authcode', methods = ['GET'])
def generate_authcode():
    return jsonify({"authcode":"123456"})

# check telephone number existance
@api.route('/businesses/check/<string:tel>', methods = ['GET'])
def check_telephone(tel):
    business = BusinessAuthenticator.query.filter_by(telephone = tel).first()
    if business:
        return jsonify({"telephone_exist":True})
    else:
        return jsonify({"telephone_exist":False})

@api.route('/businesses', methods = ['POST'])
def create_business():
    businessJson = request.json
    username = businessJson.get("username")
    telephone = businessJson.get("telephone")
    password = businessJson.get("password")

    business = BusinessAuthenticator.query.filter_by(username = username).first()
   
    # check existance 
    if business:
        return errors.conflict("username exist")
        
    business = BusinessAuthenticator.query.filter_by(telephone = telephone).first()
    if business:
        return errors.conflict("telephone exist")

    # add new business 
    business = Business(telephone = telephone)
    Business.add(business) 

    # add to business auth 
    business_auth = BusinessAuthenticator(business_id = business.id, username = username, 
                                          telephone = telephone, password = password)
    BusinessAuthenticator.add(business_auth)
    
    response = Response(json.dumps(business.toJson()), 201, mimetype = "application/json") # object to json 
    # default_external is False means relative path, True means absolute path
    response.headers.add("Location", url_for("api.get_business", id = business.id, external = True))
   
    return response 

@api.route('/businesses/<int:id>/password', methods = ['PUT', 'PATCH'])
def update_password(id):
    business = BusinessAuthenticator.query.get_or_404(id)
    new_password = request.json['password']
    business.setPassword(new_password)
    business.update()
    return jsonify(business.toJson()) 

#@api.route('/businesses/<int:id>', methods = ['DELETE'])
#def delete_business():
#    business = Business.query.get_or_404(id)
#    ret = Business.delete(business)
#    return json.dumps(ret)

@api.route('/businesses/<int:id>', methods = ['DELETE'])
def delete_business(id):
    business = Business.query.get_or_404(id)
    is_locked = request.json['is_locked']
    business.setLock(is_locked)
    business.update()
    return jsonify(business.toJson()) 
