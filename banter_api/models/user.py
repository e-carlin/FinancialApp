import jwt
import datetime
from flask import current_app
from sqlalchemy.orm import validates
from banter_api.extensions import bcrypt, db

class EmailMalformedError(Exception):
    pass

class PasswordEmptyError(Exception):
    pass

class User(db.Model):
    """ User Model for storing user related details """
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)

    @validates('email')
    def validate_email(self, key, address):
        if '@' not in address:
            raise EmailMalformedError("the email address must contain an @ symbol")
        return address

    def __init__(self, email, password):
        self.email = email.strip()
        try:
            self.password = bcrypt.generate_password_hash(
                password, current_app.config.get('BCRYPT_LOG_ROUNDS')
            )
        except ValueError as e:
            # Doing validation in here instead of in @validates because generate_password_hash would throw a ValueError before validates is called
            raise PasswordEmptyError("the password cannot be empty")
        self.registered_on = datetime.datetime.now()

    def __repr__(self):
        return '[id: {}, email: {}, password: {}, registered_on: {}'.format(self.id, self.email, self.password, self.registered_on)

    def encode_auth_token(self, user_id):
        current_app.logger.info('Encoding auth token for user_id {}'.format(user_id))
        """
        Generates the Auth Token
        :return: string
        """
        try:
            payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(days=0, seconds=5),    # TODO: Make this delta better, probably should be longer
                'iat': datetime.datetime.utcnow(),
                'sub': user_id
            }
            current_app.logger.debug('Generating auth token with payload [{}] , SECRET_KEY [{}], and algorithm HS256'.format(
                payload, current_app.config.get('SECRET_KEY')
            )) # TODO: Don't log the secret key
            return jwt.encode(
                payload,
                current_app.config.get('SECRET_KEY') ,
                algorithm='HS256'
            )
        except Exception as e:
            current_app.logger.debug("Error encoding auth token: {}".format(e))
            return e

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Validates the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, current_app.config.get('SECRET_KEY'))
            return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'


























