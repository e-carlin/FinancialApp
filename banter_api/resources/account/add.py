from plaid import Client
from plaid.errors import APIError, ItemError
from flask import request, make_response, jsonify
from flask_restful import Resource, abort
from flask import current_app
from marshmallow import Schema, fields, ValidationError
from banter_api.extensions import db
from banter_api.resources.common.parseRequest import parse_request
from banter_api.models.account import Account
from banter_api.models.institution import Institution

# from functools import wraps
# def verify_jwt(f):
#     @wraps(f)
#     def decorated_function(*args, **kws):
#         current_app.logger.debug("REQ: {}".format(request.headers))
#         if not 'Authorization' in request.headers:
#             abort(401)

#         user = None
#         data = request.headers['Authorization'].encode('ascii','ignore')
#         token = str.replace(str(data), 'Bearer ','')
#         try:
#             user = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])['sub']
#         except:
#             response_object = {
#             'status' : '401',
#             'message' : 'Authorization failed',
#             'code' : '???' #TODO:
#         }
#             abort(401, message=response_object)

#         return f(user, *args, **kws)            
#     return decorated_function
     

class AddAccountSchema(Schema):
    account_type = fields.String(required=True,
        error_messages={'required' : 'account_type is a required field'}
    )
    public_token = fields.String(required=True,
        error_messages={'required' : 'public_token is a required field'}
    )
    account_id = fields.String(required=True,
        error_messages={'required' : 'account_id is a required field'}
    )
    account_name = fields.String(required=True,
        error_messages={'required' : 'account_name is a required field'}
    )
    link_session_id = fields.String(required=True,
        error_messages={'required' : 'link_session_id is a required field'}
    )
    # TODO: We should make a nested schema to validate the fields in the accounts object
    accounts = fields.String(required=True,
        error_messages={'required' : 'accounts is a required field'}
    )
    institution_name = fields.String(required=True,
        error_messages={'required' : 'institution_name is a required field'}
    )
    institution_id = fields.String(required=True,
        error_messages={'required' : 'institution_id is a required field'}
    )
  
class AddAccountResource(Resource):
    # @verify_jwt
    def post(self):
        current_app.logger.info("Adding account information returned from Plaid.")

        data = parse_request(request, AddAccountSchema)
        current_app.logger.debug("Received this data from Plaid link: "+str(data))

        current_app.logger.info("The plaid link_session_id is '{}'".format(data['link_session_id'])) # Plaid docs recommend logging this
        exchange_response = exchange_public_token(data['public_token'])


        # save_exchange_response_data(exchange_response) # TODO

        response_object = {
            'status' : '200',
            'message' : 'Scucess exchanging public token.',
            'code' : '2002'
        }
        return response_object, 200


def get_plaid_client():
    try:
        client = Client(client_id=current_app.config.get('PLAID_CLIENT_ID'),
                        secret=current_app.config.get('PLAID_SECRET_KEY'),
                        public_key=current_app.config.get('PLAID_PUBLIC_KEY'),
                        environment=current_app.config.get('PLAID_ENV'))
    except Exception as e:
        current_app.logger.error("Error creating plaid client {}".format(e))
        response_object = {
                'status': '500',
                'message': 'Error connecting to Plaid',
                'code' : '5001'
            }
        abort(500, message=response_object)
    return client


def exchange_public_token(public_token):
    current_app.logger.debug("Exchanging plaid public token '{}' for an access token".format(public_token))
    client = get_plaid_client()
    try:
        exchange_response = client.Item.public_token.exchange(public_token)
        current_app.logger.debug("Received response from Plaid '{}'".format(exchange_response))
        current_app.logger.info("Succesfully exchanged Plaid public token for an access token and item id!")
        return exchange_response
    except Exception as e:
        current_app.logger.error("Error exchanging public token with Plaid. Exception: "+str(e)) 
        response_object = {
                'status' : '400',
                'message' : 'Error exchanging public token with Plaid',
                'code' : '4002'
            }
        abort(400, message=response_object)


def save_exchange_response_data(data):
    plaid_institution_id = data['institution']['institution_id']
    institution = Institution.query.filter_by(plaid_institution_id=plaid_institution_id).first()
    if not institution:
        current_app.logger.debug("Insitution '{}' doesn't already exist in db. Creating institution...".format(data['institution']))
        try:
            institution = Institution(
                plaid_institution_id=plaid_institution_id,
                name=data['institution']['name']
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
            abort(500, message=response_object)

    else:
        current_app.logger.debug("Institution found '{}'".format(institution))

    accounts = data['accounts']
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
  

        