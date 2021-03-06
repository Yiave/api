# coding=utf-8

from flask import jsonify, request, current_app, url_for, Response, json
import app.utils as utils
from ..aaa.errors import bad_request, unauthorized, forbidden, notfound, conflict
from app.customer.models import Customer, LocalAuthenticator
from . import customer


@customer.route("/customers", methods=["GET"])
def get_customers():
    page = request.args.get('page', 1, type=int)

    pagination = Customer.query.paginate(
        page, per_page=current_app.config['YIAVE_BUSINESSES_PER_PAGE'],
        error_out=False
    )
    customers = pagination.items
    prev = None
    if pagination.has_prev:
        prev = url_for('customer.get_customers', page=page - 1, _external=True)
    next = None
    if pagination.has_next:
        next = url_for('customer.get_customers', page=page + 1, _external=True)

    data = [b.to_json() for b in customers]
    response = Response(json.dumps(data))
    response.headers['Content-Type'] = "application/json"
    response.headers['X-Page-Pre'] = prev
    response.headers['X-Page-Next'] = next
    response.headers['X-Total-Count'] = pagination.total

    return response


@customer.route("/customers/<int:id>", methods=["GET"])
def get_customer(id):
    customer = Customer.query.get(id)
    if not customer:
        return notfound("customer not found")

    return jsonify(customer.to_json())


@customer.route("/customers/<string:username>", methods=["GET"])
def get_customer_by_username(username):
    if utils.is_email(username):
        return get_customer_by_email(username)

    customer = Customer.query.filter(Customer.username == username).first()
    if not customer:
        return notfound("User " + username + "not found")
    return jsonify(customer.to_json())


@customer.route("/customers/<string:email>", methods=["GET"])
def get_customer_by_email(email):
    customer = Customer.query.filter(Customer.email == email).first()
    if not customer:
        return notfound("User " + email + "not found")
    return jsonify(customer.to_json())


@customer.route("/customers/<int:id>", methods=["PUT", "PATCH"])
def update_customer(id):
    customer = Customer.query.get(id)
    if not customer:
        return notfound("Customer not found")

    data = request.get_json()
    if data.has_key("nickname"):
        nickname = data["nickname"]
        customer.nickname = nickname
    if data.has_key("realname"):
        realname = data["realname"]
        customer.realname = realname

    customer.update()

    return jsonify(customer.to_json())


@customer.route("/customers/<int:id>/password", methods=["PUT", "PATCH"])
def update_customer_password(id):
    customer = LocalAuthenticator.query.filter(LocalAuthenticator.customer_id == id).first()
    if not customer:
        return notfound("Customer not found")

    data = request.get_json()
    old_password = data["old_password"]
    password = data["password"]

    if old_password != customer.password:
        return forbidden("old password is wrong.")

    customer.password = password
    customer.update()

    return jsonify(customer.to_json())


if __name__ == '__main__':
    pass