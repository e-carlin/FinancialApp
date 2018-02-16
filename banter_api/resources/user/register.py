from flask_restful import Resource, abort
from flask import request, current_app
from marshmallow import Schema, fields
from sqlalchemy import exc
from banter_api.models.user import User
from banter_api.resources.common.parseRequest import parse_request

class RegisterUserSchema(Schema):
    email = fields.Email(required=True,
        error_messages={'required' : 'email is a required field'}
    )

class RegisterUserResource(Resource):
    #TODO: We should probably implement some sort of security to only accept requests
    # from our apps
    def post(self):
        """ Creates a new user"""
        data = parse_request(request, RegisterUserSchema)

        save_user(data['email'])

        response_object = {
            'status' : '200',
            'message' : 'Success registering user',
            'code' : '?????' #TODO: implement code
        }
        return response_object, 200


def save_user(email):
    current_app.logger.debug("Trying to save newly registered user to db")
    try:
        User.save_user(email)

    except exc.IntegrityError as e:
        #IntegrityError means one of the integrity constraints (ie NOT NULL, UNIQUE,...) failed
        current_app.logger.debug("Integrity error caught when registering new user. Error: {}".format(e))
        response_object = {
            'status' : '400',
            'message' : 'An integrity constraint failed when trying to save the newly registered user to the db. Please make sure the email is unique',
            'code' : '???' #TODO
        }
        abort(400, message=response_object)
    except Exception as e:
        # We should never get here
        current_app.logger.error("Fatal error trying to save user to the db. Exception: {}".format(e))
        response_object = {
            'status' : '500',
            'message' : 'There was a fatal error saving the user to the db.',
            'code' : '???' #TODO
        }
        abort(500, message=response_object)       
