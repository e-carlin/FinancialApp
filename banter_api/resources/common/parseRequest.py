from flask import current_app
from flask_restful import abort
from marshmallow import ValidationError
from json import JSONDecodeError

def parse_request(request, schema):
    try:
        schema = schema()
        data = schema.loads(request.data)
        return data
    except ValidationError as err:
        current_app.logger.error("ValidationError thrown when parsing request. Error: {}".format(err))
        
        response_object = {
            'status' : '400',
            'message' : 'Schema validation for your request failed. Failures: {}'.format(err.messages),
            'code' : '?????' #TODO: implement code
        }
        abort(400, message=response_object)
    except JSONDecodeError as err:
        current_app.logger.error("JSONDevodeErrror thrown when parsing request. Error: {}".format(err))

        response_object = {
            'status' : '400',
            'message' : 'There was an error decoding the request JSON. Please make sure the supplied JSON is valid',
            'code' : '?????' #TODO: implement code
        }
        abort(400, message=response_object)