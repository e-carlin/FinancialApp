from plaid import Client
from plaid.errors import APIError, ItemError
from flask import request, make_response, jsonify
from flask_restful import Resource
from flask import current_app
import json

from banter_api.extensions import db

class PlaidResource(Resource):
    def post(self):
        current_app.logger.info("Exchanging Plaid public token for an access token.")

        current_app.logger.debug("Converting raw request into json dict: {}".format(request.get_json))
        request_as_dict = json.loads(request.get_json())

        try:
            current_app.logger.debug("Creating Plaid Client")
            client = Client(client_id=current_app.config.get('PLAID_CLIENT_ID'),
                            secret=current_app.config.get('PLAID_SECRET_KEY'),
                            public_key=current_app.config.get('PLAID_PUBLIC_KEY'),
                            environment=current_app.config.get('PLAID_ENV'))
        except Exception as e:
            current_app.logger.error("Error creating Plaid client: {}. This likely means that constructor inputs were bad.".format(e))
            responseObject = {
                'status': 'fail',
                'message': 'Error connecting to Plaid'
            }
            return responseObject, 500
        #
        #
        try:
            current_app.logger.debug(
                "Exchanging plaid public token <{}> for an access token".format(request_as_dict['public_token']))
            public_token = request_as_dict['public_token']
            exchange_response = client.Item.public_token.exchange(public_token)
            current_app.logger.debug("Received response from Plaid [{}]".format(exchange_response))
        except Exception as e:
            current_app.logger.error("Error exchanging public token [{}] with Plaid. This probably means the public token was malformed.".format(public_token))
            responseObject = {
                'status' : 'fail',
                'message' : 'Error exchanging public token with Plaid. This probably means the public token was malformed'
            }
            return responseObject, 500
        #
        #
        # # TODO: Log the response_id (I think that is what it is called?), persist the itemID and access_token to the db
        # # print 'access token: ' + exchange_response['access_token']
        # # print 'item ID: ' + exchange_response['item_id']
        # #
        # # access_token = exchange_response['access_token']
        current_app.logger.debug("Succesfully exchanged public token with Plaid!")
        responseObject = {
            'status' : 'success',
            'message' : 'Successfully exchanged public token with Plaid.'
        }
        return responseObject, 200