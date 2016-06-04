# coding=utf-8
from ..business.models import Business, BusinessAuthenticator
from . import aaa
from flask import request, current_app, url_for, jsonify, json
from flask import Response
from ..aaa import errors
import app.utils as utils


@aaa.route('/businesses', methods=['POST'])
def create_business():
    businessJson = request.json
    name = businessJson.get("name")
    telephone = businessJson.get("telephone")
    password = businessJson.get("password")

    business = BusinessAuthenticator.query.filter_by(telephone=telephone).first()

    # check existance
    if business:
        return errors.conflict("telephone " + telephone + " exist")

    # add to business
    business = Business(telephone=telephone, name=name)
    business.add(business)

    # add to business auth
    business_auth = BusinessAuthenticator(business_id=business.id, username=telephone,
                                          telephone=telephone, password=password)
    business_auth.add(business_auth)

    response = Response(json.dumps(business.to_json()), 201, mimetype="application/json")  # object to json
    # default_external is False means relative path, True means absolute path
    response.headers.add("Location", url_for("business.get_business", id=business.id, _external=True))

    return response


# generate telephone authcode
@aaa.route('/businesses/generate_authcode', methods=['GET'])
def generate_authcode():
    return jsonify({"authcode": "123456"})


if __name__ == '__main__':
    pass
