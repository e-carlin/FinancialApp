from flask import current_app
from banter_api.extensions import bcrypt, db

class Institution(db.Model):
    __tablename__ = "institutions"

    #TODO: To be properly normalized name and paid_ins_id should really be pulled out into their own table
    # They will be repeated across institutions (ie two different users each have an account at Bank of America)
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    plaid_access_token = db.Column(db.String(255), nullable=False)
    plaid_item_id = db.Column(db.String(255), nullable=False)
    plaid_ins_id = db.Column(db.String(255), nullable=False)

    def __init__(self, name, access_token, plaid_item_id, plaid_ins_id):
        self.name = name
        self.access_token = access_token
        self.plaid_item_id = plaid_item_id
        self.plaid_ins_id = plaid_ins_id

    def __repr__(self):
        return 'id: {}, name: {}, plaid_item_id: {}, plaid_ins_id: {}'.format(self.id, self.name, self.plaid_item_id, self.plaid_ins_id)
