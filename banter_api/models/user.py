from datetime import datetime, timezone 
from flask import current_app
from sqlalchemy import exc
from banter_api.extensions import bcrypt, db

class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    registered_on = db.Column(db.DateTime(timezone=True), nullable=False)
    last_login = db.Column(db.DateTime(timezone=True))

    def __init__(self, email):
        self.email = email
        # TODO: We are storing registered_on and last_login as UTC timestamps. So we lose what timezone events actually ocurred in
        # This is fine for MVP but will need to think about it more in the future.
        self.registered_on = datetime.now(timezone.utc)

    def __repr__(self):
        return '[id: {}, email: {}'.format(self.id, self.email)

    @staticmethod
    def save_user(email):
        user = User(email)
        db.session.add(user)
        db.session.commit()


























