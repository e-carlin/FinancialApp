import os

from flask import Flask
from flask_restful import Api
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS

# from banter_api.api.endpoints.user import RegisterEndpoint

app = Flask(__name__)
CORS(app)

app_settings = os.getenv(
    'BANTER_SETTINGS',
    'app.api.config.DevelopmentConfig'
)
app.config.from_object(app_settings)

bcrypt = Bcrypt(app)
db = SQLAlchemy(app)

api = Api(app)
# api.add_resource(RegisterEndpoint, '/register')