from banter_api.extensions import  db
class Account(db.Model):
    """Account model"""
    __tablename__ = "accounts"

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    plaid_account_id = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
