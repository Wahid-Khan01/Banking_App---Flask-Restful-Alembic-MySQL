from app import db
class User(db.Model):
    __tablename__ = "user"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    mobile_number = db.Column(db.String(20), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    account_details = db.relationship('AccountDetails', backref='user', uselist=False, lazy=True)
    transactions = db.relationship('Transaction', backref='user', lazy=True)
from app.models.account_details_model import AccountDetails
from app.models.transaction_model import Transaction
