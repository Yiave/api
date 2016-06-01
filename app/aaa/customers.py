# coding=utf-8

from flask import jsonify, request, current_app, url_for, Response, json
import app.utils as utils
from .errors import bad_request, unauthorized, forbidden, notfound, conflict
from app.customer.models import Customer, LocalAuthenticator
from .email import send_email
from . import aaa


@aaa.before_app_request
def before_request():
    # if not request.headers.get("Authorization"):
    #     return unauthorized("Unauthorized API")
    pass

@aaa.after_app_request
def after_request(response):
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS")
    response.headers.add('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Credentials', 'true')
    response.headers.add('Content-Type', 'application/json')
    return response

@aaa.route('/customers', methods=['POST'])
def create_customer():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    telephone = data.get("telephone")
    password = data.get("password")

    customer = LocalAuthenticator.query.filter(LocalAuthenticator.username == username).first()
    if customer:
        return conflict("username exist")

    customer = LocalAuthenticator.query.filter(LocalAuthenticator.email == email).first()
    if customer:
        return conflict("email exist")

    # add to customer table
    customer = Customer(username=username, email=email, telephone=telephone,
                        signup_date=utils.getDatetime())
    customer.add(customer)

    # add to local_auth table
    localAuthenticator = LocalAuthenticator(customer_id=customer.id, username=username, email=email,
                                            telephone=telephone, password=password)
    localAuthenticator.add(localAuthenticator)

    # send confirm email
    confirm_token = customer.get_confirm_token()
    send_email(customer.email, "Confirm Your Account", "confirm", user=customer, token=confirm_token)

    response = Response(json.dumps(customer.toJSON()), status=201, mimetype="application/json")
    response.headers.add("Location", url_for("aaa.get_customer", id=customer.id, _external=True))

    return response


@aaa.route("/customers/confirm/<token>", methods=["GET"])
def confirm(token):
    data = request.get_json()
    email = data.get("email")

    customer = Customer.query.filter(Customer.email == email).first()
    if customer.set_confirmed(token):
        return jsonify(customer.toJSON())
    else:
        return unauthorized("The confirmation link is invalid or has expired.")


@aaa.route('/customers/authenticate', methods=["POST"])
def authenticate_customer():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    customer = Customer.query.filter(Customer.username == username)
    if password != password:
        return forbidden("Wrong password")

    return jsonify(customer.toJSON())


@aaa.route("/customers/<int:id>", methods=["GET"])
def get_customer(id):
    customer = Customer.query.get(id)
    if not customer:
        return notfound("customer not found")

    return jsonify(customer.toJSON())


if __name__ == '__main__':
    pass
