import os
from flask import Flask
from flask_restful import Api
from flask_cors import CORS

from .extensions import db, bcrypt
from banter_api.resources.account.add import AddAccountResource
from banter_api.resources.user.register import RegisterUserResource


def create_app():
    app = Flask(__name__)
    app.config.from_object('banter_api.config.DevelopmentConfig') #TODO: Read this from env var
    CORS(app)

    register_extensions(app)

    api = Api(app)
    add_resources(api)
    return app

def register_extensions(app):
    db.init_app(app)
    bcrypt.init_app(app)

def add_resources(api):
    api.add_resource(AddAccountResource, '/account/add')
    api.add_resource(RegisterUserResource, '/user/register')
