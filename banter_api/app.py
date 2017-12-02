import os

from flask import Flask
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from banter_api.resources.user import RegisterResource
# app = Flask(__name__)
# CORS(app) # TODO: DO I NEED THIS IS THIS SAFE??
#
# app_settings = os.getenv(
#     'BANTER_SETTINGS',
#     'banter_api.config.DevelopmentConfig'
# )
# app.config.from_object(app_settings)
#
# bcrypt = Bcrypt(app)
# db = SQLAlchemy(app)
# api = Api(app)



############################
from .extensions import db, bcrypt


def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ['BANTER_SETTINGS'])
    # app.debug = True
    # app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # TODO: This used to live in config.py
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://banterapiuser:@localhost/banter'  # TODO: This used to live in config.py

    register_extensions(app)

    api = Api(app)
    register_resources(api)
    return app

def register_extensions(app):
    db.init_app(app)
    bcrypt.init_app(app)

def register_resources(api):
    api.add_resource(RegisterResource, '/register')
