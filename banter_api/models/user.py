import datetime
from flask import current_app
from banter_api.extensions import bcrypt, db

class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cognito_id = db.Column(db.String(255), unique=True, nullable=False)

    def __init__(self, cognito_id):
        self.cognito_id = cognito_id

    def __repr__(self):
        return '[id: {}, cognito_id: {}'.format(self.id, self.cognito_id)



























