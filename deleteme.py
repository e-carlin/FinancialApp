# from marshmallow import ValidationError, Schema, fields

# class BandMemberSchema(Schema):
#     name = fields.String(required=True)
#     email = fields.Email()

# user_data = [
#     {'email': 'mick@stones.com', 'name': 'Mick'},
#     {'email': 'invalid', 'name': 'Invalid'},  # invalid email
#     {'email': 'keith@stones.com', 'name': 'Keith'},
#     {'email': 'charlie@stones.com'},  # missing "name"
# ]

# try:
#     BandMemberSchema(many=True).load(user_data)
#     print("loaded")
# except ValidationError as err:
#     print("Here")
#     print(err.messages)

# res = BandMemberSchema(many=True).load(user_data)
# print("RES: {}".format(res))

from datetime import datetime, timezone 
print(datetime.now(timezone.utc))