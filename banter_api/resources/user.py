from flask import request, make_response, jsonify
from flask_restful import Resource

from banter_api.extensions import db
from banter_api.models import User

class RegisterResource(Resource):
    def post(self):
        print("**** IN REGISTER ****")
        # get the post data
        post_data = request.get_json()
        print("DATA IS "+str(post_data))
        # check if user already exists
        user = User.query.filter_by(email=post_data.get('email')).first()
        print('**** USER IS '+str(user))
        if not user:
            print("*** IN NOT USER***")
            try:
                print("*** EMAIL IS "+post_data.get('email'))
                print("**** PASS IS "+post_data.get('password'))
                user = User(
                    email=post_data.get('email'),
                    password=post_data.get('password')
                )
                print("SECOND USER IS "+str(user))
                # insert the user
                db.session.add(user)
                db.session.commit()
                print("***** USER HAS BEEN SAVE ****")
                # generate the auth token
                auth_token = user.encode_auth_token(user.id)
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'auth_token': auth_token.decode()
                }
                print("******* RESP *******"+str(responseObject))
                return responseObject, 201
            except Exception as e:
                print("**** THERE WAS AN EXCEPTION **** ")
                print(e)
                print("************")
                responseObject = {
                    'status': 'fail',
                    'message': 'Some error occurred. Please try again.'
                }
                return responseObject, 401
        else:
            responseObject = {
                'status': 'fail',
                'message': 'User already exists. Please Log in.',
            }
            return responseObject, 201 # TODO: Should this be 201?



# api.add_resource(RegisterEndpoint, '/register')


