from flask import request, make_response, jsonify
from flask_restful import Resource
from flask import current_app

from banter_api.extensions import db
from banter_api.models import User

class RegisterResource(Resource):
    def post(self):
        # get the post data
        post_data = request.get_json()
        current_app.logger.info('Trying to register user {}'.format(post_data.get('email')))
        # check if user already exists
        user = User.query.filter_by(email=post_data.get('email')).first()
        if not user:
            current_app.logger.info("User doesn't already exist in db. Creating user...")
            try:
                user = User(
                    email=post_data.get('email'),
                    password=post_data.get('password')
                )
                # insert the user
                db.session.add(user)
                db.session.commit()
                current_app.logger.debug("Saved user to db.")
                # generate the auth token
                auth_token = user.encode_auth_token(user.id)
                current_app.logger.debug("Created auth token {} ".format(auth_token.decode()))
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'auth_token': auth_token.decode()
                }
                return responseObject, 201
            except Exception as e:
                current_app.logger.debug("Error creating user {}".format(e))
                responseObject = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.'
                }
                return responseObject, 401
        else:
            current_app.logger.info("The email {} already exists in the db under user {}".format(post_data.get('email') , user))
            responseObject = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.',
            }
            return responseObject, 201 # TODO: Should this be 201?