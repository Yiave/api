# coding=utf-8
from flask import jsonify, request, current_app, url_for, Response, json
import app.utils as utils
from .errors import bad_request, unauthorized, forbidden, notfound, conflict
from app.customer.models import Customer, LocalAuthenticator
from .email import send_email
from . import aaa


@aaa.route('/customers', methods=['POST'])
def create_customer():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    telephone = data.get("telephone")
    password = data.get("password")

    customer = LocalAuthenticator.query.filter(LocalAuthenticator.username == username).first()
    if customer:
        return conflict("username " + username + " exist")

    customer = LocalAuthenticator.query.filter(LocalAuthenticator.email == email).first()
    if customer:
        return conflict("email " + email + " already registed")

    # add to customer table
    customer = Customer(username=username, email=email, telephone=telephone,
                        signup_date=utils.get_datetime())
    customer.add(customer)

    # add to local_auth table
    localAuthenticator = LocalAuthenticator(customer_id=customer.id, username=username, email=email,
                                            telephone=telephone, password=password)
    localAuthenticator.add(localAuthenticator)

    # send confirm email
    confirm_token = customer.get_confirm_token()
    send_email(customer.email, "Confirm Your Account", "confirm", user=customer, token=confirm_token)

    response = Response(json.dumps(customer.to_json()), status=201, mimetype="application/json")
    response.headers.add("Location", url_for("customer.get_customer", id=customer.id, _external=True))

    return response


@aaa.route("/customers/<int:id>/confirm/<string:token>", methods=["GET"])
def confirm(id, token):
    customer = Customer.query.get(id)
    if customer.set_confirmed(token):
        return jsonify(customer.to_json())
    else:
        return unauthorized("The confirmation link is invalid or has expired.")


@aaa.route('/customers/authenticate', methods=["POST"])
def authenticate_customer():
    data = request.get_json()
    username = data.get("username")
    email = data.get("email")
    password = data.get("password")

    customer = None
    if username is not None:
        customer = LocalAuthenticator.query.filter(LocalAuthenticator.username == username).first()
        if password != customer.password:
            return forbidden("Wrong password for " + username)
    elif email is not None:
        customer = LocalAuthenticator.query.filter(LocalAuthenticator.email == email).first()
        if password != customer.password:
            return forbidden("Wrong password for " + email)

    customer = Customer.query.get(customer.customer_id)
    customer.set_last_signin_date()

    return jsonify(customer.to_json())


if __name__ == '__main__':
    pass
