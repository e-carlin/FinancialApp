from flask_restful import Resource, abort
from flask import request, current_app
from marshmallow import Schema, fields, ValidationError, pprint
from json import JSONDecodeError
from sqlalchemy import exc
from banter_api.models.user import User

class UserSchema(Schema):
    email = fields.Email(required=True,
        error_messages={'required' : 'email is a required field'}
    )

class UserResource(Resource):
    #TODO: We should probably implement some sort of security to only accept requests
    # from our apps
    def post(self):
        """ Creates a new user"""
        data = parse_request(request)

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
    except Exception as e:
        current_app.logger.error("Could not save newly registered user to db. Exception: {}".format(e))
        if type(e) is exc.IntegrityError:
            #IntegrityError means one of the integrity constraints (ie NOT NULL, UNIQUE,...) failed
            response_object = {
                'status' : '400',
                'message' : 'An integrity constraint failed when trying to save the newly registered user to the db. Please make sure the email is unique',
                'code' : '???' #TODO
            }
            abort(400, message=response_object)

        else:
            # We should never get here
            current_app.logger.error("Fatal error trying to save user to the db. Exception: {}".format(e))
            response_object = {
                'status' : '500',
                'message' : 'There was a fatal error saving the user to the db.',
                'code' : '???' #TODO
            }
            abort(500, message=response_object)       

def parse_request(request):
    try:
        schema = UserSchema()
        data = schema.loads(request.data)
        current_app.logger.debug("Data is: {}".format(data))
        
        #TODO: This is a big time hack that has to be done unless marhmallow is intalled with the --pre flag.
        # If it is installed with --pre then the ValidationError exception below will catch this
        if data[1]:
            current_app.logger.debug("Errors found when parsing request. Error: {}".format(data[1]))
            response_object = {
                'status' : '400',
                'message' : 'Schema validation for your request failed. Failures: {}'.format(data[1]),
                'code' : '?????' #TODO: implement code
            }
            abort(400, message=response_object)

        return data[0]
    except ValidationError as err:
        current_app.logger.debug("ValidationError thrown when parsing request. Error: {}".format(err))
        
        response_object = {
            'status' : '400',
            'message' : 'Schema validation for your request failed. Failures: {}'.format(err.messages),
            'code' : '?????' #TODO: implement code
        }
        abort(400, message=response_object)
    except JSONDecodeError as err:
        current_app.logger.debug("JSONDevodeErrror thrown when parsing request. Error: {}".format(err))

        response_object = {
            'status' : '400',
            'message' : 'There was an error decoding the request JSON. Please make sure you JSON is valid',
            'code' : '?????' #TODO: implement code
        }
        abort(400, message=response_object)
