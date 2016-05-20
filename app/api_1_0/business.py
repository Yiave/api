from ..models import Business 
from . import api
from flask import request, current_app, url_for, jsonify, json
from flask import Response

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
def getBusiness(id):
    business = Business.query.get_or_404(id)
    return jsonify(business.toJson()) # string to json 


@api.route('/businesses', methods = ['POST'])
def setBusiness():
    businessJson = request.json
    Business.add(Business.fromJson(businessJson))
    return json.dumps(businessJson)# object to json 

@api.route('/businesses/<int:id>', methods = ['PUT', 'PATCH'])
def updateBusiness(id):
    business = Business.query.get_or_404(id)
    newName = request.json['name']
    business.setName(newName)
    business.update()
    return jsonify(business.toJson()) 

#@api.route('/businesses/<int:id>', methods = ['DELETE'])
#def delete_business():
#    business = Business.query.get_or_404(id)
#    ret = Business.delete(business)
#    return json.dumps(ret)

@api.route('/businesses/<int:id>', methods = ['DELETE'])
def deleteBusiness(id):
    business = Business.query.get_or_404(id)
    is_locked = request.json['is_locked']
    business.setLock(is_locked)
    business.update()
    return jsonify(business.toJson()) 
