# coding: utf-8
from flask import Flask
from flask_restless import APIManager
from flask_sqlalchemy import SQLAlchemy
from flask_jwt import JWT, jwt_required, current_identity
from flask_cors import CORS, cross_origin

import logging
logging.basicConfig()

class AuthenticatedUser():
    id = 0
    email = ""

    def __init__(self, id, email):
        self.id = id
        self.email = email

def authenticate(username, password):
    user = User.query.filter_by(email=username, password=password).first()
    if user:
        user_dict = user.to_dict()
        return AuthenticatedUser(user_dict["id"], user_dict["email"])

def identity(payload):
    logging.info(payload)
    user_id = payload['identity']
    return User.query.filter_by(id=user_id).first()

app = Flask(__name__)
db = SQLAlchemy(app)
CORS(app)
jwt = JWT(app, authenticate, identity)
print(jwt)

rest_manager = APIManager()
from user_service.views import *
from user_service.errors import *

def init_app(settings='user_service.config'):
    app.config.from_object(settings)
    db.init_app(app)
    rest_manager.init_app(app, session=db.session, flask_sqlalchemy_db=db)
