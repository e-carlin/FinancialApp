import os

from flask import Flask
from flask_restful import Api
# from flask_bcrypt import Bcrypt
# from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from .extensions import db, bcrypt

from banter_api.resources.user import RegisterResource
from banter_api.resources._plaid import PlaidResource


def create_app():
    app = Flask(__name__)
    app.config.from_object(os.environ['BANTER_SETTINGS'])
    CORS(app)

    register_extensions(app)

    api = Api(app)
    add_resources(api)
    return app

def register_extensions(app):
    db.init_app(app)
    bcrypt.init_app(app)

def add_resources(api):
    api.add_resource(RegisterResource, '/register')
    api.add_resource(PlaidResource, '/exchange_plaid_public_token')
