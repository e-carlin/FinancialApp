from flask_restful import Resource, abort
from flask import request, current_app
from marshmallow import Schema, fields, ValidationError, pprint
from json import JSONDecodeError

class UserSchema(Schema):
    cognito_id = fields.Str(required=True,
        error_messages={"required" : "cognito_id is a required field"}
    )

class UserResource(Resource):
    def post(self):
        """ Creates a new user"""
        data = parse_request(request)

        # TODO: Implement

        response_object = {
            'status' : '200',
            'message' : 'Success registering user',
            'code' : '?????' #TODO: implement code
        }
        return response_object, 200

def parse_request(request):
    try:
        schema = UserSchema()
        data = schema.loads(request.data)
        current_app.logger.debug("Data is: {}".format(data))
        return data
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
