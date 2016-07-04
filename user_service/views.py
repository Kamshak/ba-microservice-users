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

rest_manager.create_api(User, methods=['GET', 'POST', 'PUT'], preprocessors=dict(GET_MANY=[authenticator()], GET_SINGLE=[authenticator()], PUT_SINGLE=[authenticator()]))
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
@jwt_required()
def get_default_address(customer_id):
    address = Address.query.filter_by(customer_id=customer_id).first()
    if address:
        return jsonify(address.to_dict()), 200
    abort(404)

@app.route("/api/users/email/<email>", methods=['GET'])
@jwt_required()
def find_user_by_email(email):
    user = User.query.filter_by(email=email).first()
    if user:
        return jsonify(user.to_dict()), 200
    abort(404)
