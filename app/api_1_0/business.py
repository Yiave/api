from ..models import Business, BusinessAuthenticator 
from . import api
from flask import request, current_app, url_for, jsonify, json
from flask import Response
from . import errors 

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


@api.route('/businesses', methods = ['POST'])
def create_business():
    businessJson = request.json
    username = businessJson.get("name")
    telephone = businessJson.get("telephone")
    password = businessJson.get("password")

    business = BusinessAuthenticator.query.filter_by(username = username).first()
   
    # check existance 
    if business:
        if business['username'] == username:
            return errors.conflict("username exist")
        
        if business['telephone'] == telephone:
            return errors.conflict("telephone exist")
  
    # send telephone auth number
    #TODO 

    # add new business 
    business = Business(username = username, telephone = telephone)
    Business.add(business) 

    # add to business auth 
    business_auth = BusinessAuthenticator(business_id = business.id, username = username, 
                                          telephone = telephone, password = password)
    BusinessAuthenticator.add(business_auth)
    
    response = Response(json.dumps(business), 201, mimetype = "application/json") # object to json 
    response.headers.add("Location", url_for(get_business, id = business.id, external = True)) 
    # 默认_external 为False，表示生成相对路径；为True 时，表示生成绝对路径
   
    return response 

@api.route('/businesses/<int:id>', methods = ['PUT', 'PATCH'])
def update_business(id):
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
def delete_business(id):
    business = Business.query.get_or_404(id)
    is_locked = request.json['is_locked']
    business.setLock(is_locked)
    business.update()
    return jsonify(business.toJson()) 
