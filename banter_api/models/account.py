from flask import current_app
from banter_api.extensions import bcrypt, db

class Account(db.Model):
    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    institution_id = db.Column(db.Integer, db.ForeignKey("institutions.id"), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    plaid_id = db.Column(db.String(255), nullable=False)
    account_type = db.Column(db.String(255), nullable=False)
    current_balance = db.Column(db.Numeric, nullable=False, default=0.0)
    available_balance = db.Column(db.Numeric, nullable=False, default=0.0)      

    def __init__(self, user_id, institution_id, name,  plaid_id, account_type, current_balance, available_balance):
        self.user_id = user_id
        self.institution_id = institution_id
        self.name = name
        self.plaid_id = plaid_id
        self.account_type = account_type
        self.current_balance = current_balance
        self.available_balance = available_balance

    def __repr__(self):
        return 'id: {}, user_id: {}, institution_id: {}, name: {}, plaid_id: {}, account_type: {}, current_balance: {}, available_balance: {}'.format(self.id, self.user_id, self.institution_id, self.name, self.plaid_id, self.account_type, self.current_balance, self.available_balance)
