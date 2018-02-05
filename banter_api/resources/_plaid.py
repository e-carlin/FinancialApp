from plaid import Client
from plaid.errors import APIError, ItemError
from flask import request, make_response, jsonify
from flask_restful import Resource
from flask import current_app

from banter_api.extensions import db
from banter_api.models.institution import Institution
from banter_api.models.account import Account

class PlaidResource(Resource):
    def post(self):
        current_app.logger.info("Exchanging Plaid public token for an access token and item id.")

        request_as_dict = request.get_json()
        current_app.logger.debug("Converting raw request into json dict: '{}'".format(request_as_dict))

        try:
            current_app.logger.debug("Creating Plaid Client")
            client = Client(client_id=current_app.config.get('PLAID_CLIENT_ID'),
                            secret=current_app.config.get('PLAID_SECRET_KEY'),
                            public_key=current_app.config.get('PLAID_PUBLIC_KEY'),
                            environment=current_app.config.get('PLAID_ENV'))
        except Exception as e:
            current_app.logger.error("Error creating Plaid client: '{}'. "
                                     "This likely means that the client constructor inputs were bad.".format(e))
            responseObject = {
                'status': '500',
                'message': 'Error connecting to Plaid',
                'code' : '5001'
            }
            return responseObject, 500

        try:
            public_token = request_as_dict['public_token']
            current_app.logger.debug("Exchanging plaid public token '{}' for an access token"
                                     .format(public_token))

            exchange_response = client.Item.public_token.exchange(public_token)
            current_app.logger.debug("Received response from Plaid '{}'".format(exchange_response))
        except Exception as e:
            current_app.logger.error("Error exchanging public token with Plaid. This probably means the public token was malformed.")
            current_app.logger.error(e)
            responseObject = {
                'status' : '400',
                'message' : 'Error exchanging public token with Plaid. This probably means the public token was malformed',
                'code' : '4002'
            }
            return responseObject, 400

        current_app.logger.info("Succesfully exchanged Plaid public token for an access token and item id!")
        current_app.logger.debug("The plaid link_session_id is '{}'".format(request_as_dict['metadata']['link_session_id']))

        plaid_institution_id = request_as_dict['metadata']['institution']['institution_id']
        institution = Institution.query.filter_by(plaid_institution_id=plaid_institution_id).first()
        if not institution:
            current_app.logger.debug("Insitution '{}' doesn't already exist in db. Creating institution...".format(request_as_dict['metadata']['institution']))
            try:
                institution = Institution(
                    plaid_institution_id=plaid_institution_id,
                    name=request_as_dict['metadata']['institution']['name']
                )
                db.session.add(institution)
                db.session.commit()
                current_app.logger.debug("Saved institution '{}' to db".format(institution))
            except Exception as e:
                current_app.logger.error("Error creating institution '{}'".format(institution))
                response_object = {
                    'status' : '500',
                    'message' : 'There was an error saving the institution. Please try again.',
                    'code' : '5002'
                }
                return response_object, 500

        else:
            current_app.logger.debug("Institution found '{}'".format(institution))

        accounts = request_as_dict['metadata']['accounts']
        current_app.logger.debug("Saving accounts '{}' to db.".format(accounts))

        for accountDetails in accounts:
            current_app.logger.debug("Trying to save account {}.".format(accountDetails))
            plaid_account_id = accountDetails['id']
            if not Account.query.filter_by(plaid_account_id=plaid_account_id).first(): # If an account with this id is *not* already found
                try:
                    account = Account(
                        plaid_account_id = plaid_account_id,
                        name = accountDetails["name"]
                    )
                    db.session.add(account)
                    db.session.commit()
                    current_app.logger.info("Saved account {}".format(accountDetails))
                except Exception as e:
                    current_app.logger.error("Error saving account {}. \n {}".format(accountDetails, e)) # TODO: Should this be str(e)


        response_object = {
            'status' : '200',
            'message' : 'Scucess exchanging public token.',
            'code' : '2002'
        }
        return response_object, 200