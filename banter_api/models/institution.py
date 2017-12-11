from flask import current_app
from banter_api.extensions import bcrypt, db


class Institution(db.Model):
    """ Insitution model """
    __tablename__ = "institutions"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    plaid_institution_id = db.Column(db.String(255), unique=True, nullable=False)
    name = db.Column(db.String(255), unique=True, nullable=False)

    def __init__(self, plaid_institution_id, name):
        self.plaid_institution_id = plaid_institution_id
        self.name = name

    def __repr__(self):
        return "'id: {}, plaid_institution_id: {}, name: {}'".format(self.id, self.plaid_institution_id, self.name)





























