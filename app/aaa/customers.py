# coding=utf-8

from flask import jsonify, request, current_app, url_for, Response, json
import app.utils as utils
import app.aaa.errors as erros
from app.api_1_0 import api
from app.models import Customer, LocalAuthenticator
from .email import send_email


@api.before_app_request
def before_request():
    if not request.headers.get("Authorization"):
        return erros.unauthorized("Unauthorized API")


@api.route('/customers', methods=['POST'])
def create_customer():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    telephone = data.get("telephone")
    password = data.get("password")

    customer = LocalAuthenticator.query.filter(LocalAuthenticator.username == username).first()
    if customer:
        return erros.conflict("username exits")

    customer = LocalAuthenticator.query.filter(LocalAuthenticator.email == email).first()
    if customer:
        return erros.conflict("email exits")

    # add to customer table
    customer = Customer(username=username, email=email, telephone=telephone, password=password,
                        signup_date=utils.getDatetime())
    customer.add(customer)

    # add to local_auth table
    localAuthenticator = LocalAuthenticator(customer_id=customer.id, username=username, email=email,
                                            telephone=telephone, password=password)
    localAuthenticator.add(customer)

    # send confirm email
    confirm_token = customer.get_confirm_token()
    send_email(customer.email, "Confirm Your Account", "confirm", user=customer, token=confirm_token)

    response = Response(json.dumps(customer), 201, mimetype="application/json")
    response.headers.add("Location", url_for(get_customer, id=customer.id, _external=True))

    return response


@api.route("/customers/confirm/<token>")
def confirm(token):
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    customer = Customer.query.filter(Customer.email == email).first()
    if customer.set_confirmed(token):
        return jsonify(customer.toJSON())
    else:
        return erros.unauthorized("confirm failed")


@api.route('/customers/authenticate')
def authenticate_customer():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    customer = Customer.query.filter(Customer.username == username)
    if password != password:
        return erros.forbidden("Wrong password")

    return jsonify(customer.toJSON())


@api.route("/customers/<int:id>")
def get_customer(id):
    customer = Customer.query.get(id)
    if not customer:
        return erros.notfound("customer not found")

    return jsonify(customer.toJSON())


if __name__ == '__main__':
    pass
