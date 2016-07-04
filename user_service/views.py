# coding: utf-8
from .models import User, Role
from flask import request, jsonify, abort
from user_service import app, rest_manager
from datetime import datetime
from user_service.models import Country, Region, City, Customer, Address
from flask_jwt import JWT, jwt_required, current_identity
from flask.ext.restless import ProcessingException
import logging
logging.basicConfig()

def authenticator():
    def check_auth(instance_id=None, **kwargs):
        logging.error(kwargs)
        if (instance_id == None):
            raise ProcessingException(description='Not Authorized', code=401)
        if (instance_id != current_identity.id):
            raise ProcessingException(description='Not Authorized', code=401)

    return jwt_required()(check_auth)

rest_manager.create_api(User, methods=['GET', 'POST'], preprocessors=dict(GET_MANY=[authenticator()], GET_SINGLE=[authenticator()]))
#rest_manager.create_api(Role, methods=['GET', 'POST'])
#rest_manager.create_api(Country, methods=['GET', 'POST', 'PUT', 'DELETE'])
#rest_manager.create_api(Region, methods=['GET', 'POST', 'PUT', 'DELETE'])
#rest_manager.create_api(City, methods=['GET', 'POST', 'PUT', 'DELETE'])
#rest_manager.create_api(Customer, methods=['GET', 'POST', 'PUT', 'DELETE'])
#rest_manager.create_api(Address, methods=['GET', 'POST', 'PUT', 'DELETE'])


@app.route("/")
def index():
    return "OK"


@app.route("/api/customers/<customer_id>/address", methods=['GET'])
def get_default_address(customer_id):
    address = Address.query.filter_by(customer_id=customer_id).first()
    if address:
        return jsonify(address.to_dict()), 200
    abort(404)


@app.route("/api/users/login", methods=['POST'])
def login():
    email = request.json['email']
    password = request.json['password']
    user = User.query.filter_by(email=email, password=password).first()
    if user:
        login_user(user)
        return jsonify(user.to_dict()), 200


@app.route("/api/users/email/<email>", methods=['GET'])
def find_user_by_email(email):
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify(user.to_dict()), 200
    abort(404)


@app.route("/api/users/logout", methods=['POST'])
def logout():
    user_id = request.json['user_id']
    user = User.get_by_id(user_id)
    user.last_login_at = user.current_login_at
    user.current_login_at = None
    user.last_login_ip = user.current_login_ip
    user.current_login_ip = None
    user.save()
    return jsonify({'status': 'OK'})


def login_user(user):
    if 'X-Forwarded-For' not in request.headers:
        remote_addr = request.remote_addr or 'untrackable'
    else:
        remote_addr = request.headers.getlist("X-Forwarded-For")[0]
    old_current_login, new_current_login = user.current_login_at, datetime.utcnow()
    old_current_ip, new_current_ip = user.current_login_ip, remote_addr

    user.last_login_at = old_current_login or new_current_login
    user.current_login_at = new_current_login
    user.last_login_ip = old_current_ip or new_current_ip
    user.current_login_ip = new_current_ip
    user.login_count = user.login_count + 1 if user.login_count else 1
    user.save()
