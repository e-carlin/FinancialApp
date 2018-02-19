from datetime import datetime, timezone 
from flask import current_app
from banter_api.extensions import bcrypt, db

class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    signed_up_on = db.Column(db.DateTime(timezone=True), nullable=False)
    last_sign_in = db.Column(db.DateTime(timezone=True))

    def __init__(self, email):
        self.email = email
        # TODO: We are storing signed_up_on and last_sign_in as UTC timestamps. So we lose what timezone events actually ocurred in
        # This is fine for MVP but will need to think about it more in the future.
        self.signed_up_on = datetime.now(timezone.utc)

    def __repr__(self):
        return '[id: {}, email: {}'.format(self.id, self.email)

    @staticmethod
    #TODO: this should probably be a @classmethod and we should be using self instead of creating a new user
    def save_user(email):
        user = User(email)
        db.session.add(user)
        db.session.commit()
