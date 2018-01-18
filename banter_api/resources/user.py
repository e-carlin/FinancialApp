from flask import request, make_response, jsonify
from flask_restful import Resource
from flask import current_app

from banter_api.extensions import db
from banter_api.models.user import User, EmailMalformedError, PasswordEmptyError

class RegisterResource(Resource):
    def post(self):
        # get the post data
        post_data = request.get_json()
        current_app.logger.info("Trying to register user: {}".format(post_data.get('email')))
        current_app.logger.debug("Full request body was: '{}'".format(post_data))
        # check if user already exists
        user = User.query.filter_by(email=post_data.get("email")).first()
        if not user:
            current_app.logger.info("User doesn't already exist in db. Creating user...")
            try:
                user = User(
                    email=post_data.get("email"),
                    password=post_data.get("password")
                )
                # insert the user
                db.session.add(user)
                db.session.commit()
                current_app.logger.debug("Saved user to db.")
                # generate the auth token
                auth_token = user.encode_auth_token(user.id)
                current_app.logger.debug("Created auth token: {} ".format(auth_token.decode()))
                responseObject = {
                    'status': '201',
                    'message': 'Successfully registered user',
                    'auth_token': auth_token.decode(),
                    'internal_code': '2001'
                }
                return responseObject, 201
            except EmailMalformedError as e:
                current_app.logger.error("Supplied email was malformed: {}".format(e))
                responseObject = {
                    'status': '400',
                    'message': "Error registering user, {}".format(e),
                    'internal_code': '4000'
                }
                return responseObject, 400
            except PasswordEmptyError as e:
                current_app.logger.error("Supplied password was malformed, {}".format(e))
                responseObject = {
                    'status': '400',
                    'message': "Error registering user, {}".format(e),
                    'internal_code' : '4001'
                }
                return responseObject, 400
            except Exception as e:
                current_app.logger.error("Unhandled error registering user, {}".format(e))
                responseObject = {
                    'status': '500',
                    'message': 'There was an error registering. Please try again.',
                    'internal_code' : '5000'
                }
                return responseObject, 500
        else:
            current_app.logger.info("The email {} already exists in the db under user {}".format(post_data.get('email') , user))
            responseObject = {
                'status': '409',
                'message': 'Sorry, the email is already taken. Please try another or log in.',
                "code" : "4002"
            }
            return responseObject, 409