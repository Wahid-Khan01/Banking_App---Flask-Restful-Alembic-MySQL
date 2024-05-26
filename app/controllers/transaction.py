from flask import request
from app import db
from app.models.user_model import User
from app.models.account_details_model import AccountDetails
from app.models.transaction_model import Transaction
from app.serde.transaction_schema import transaction_schema, transaction_list_schema
from marshmallow import ValidationError
from datetime import datetime
from app.controllers.base_class import Base

class TransactionAPI(Base):
    def post(self):
        data = request.json

        if not data:
            return {'message':'No data provided'}
        if not data.get('location'):
            return {'message':'location field cannot be empty'}

        try:
            validated_data = transaction_schema.load(data)
        except ValidationError as e:
            return {'message': 'Validation Error', 'errors': e.messages}, 400

        user_id = request.user_id
        user = User.query.get(user_id)
        if not user:
            return {'message': 'User not found'}, 404

        account = AccountDetails.query.filter_by(user_id=user_id).first()
        if not account:
            return {'message': 'Account details not found'}, 404

        if validated_data.get('debit'):
            if account.balance < validated_data['debit']:
                return {'message': 'Insufficient balance'}, 400
            account.balance -= validated_data['debit']
        if validated_data.get('credit'):
            account.balance += validated_data['credit']

        transaction = Transaction(
            debit=validated_data.get('debit'),
            credit=validated_data.get('credit'),
            debit_type=validated_data.get('debit_type'),
            credit_type=validated_data.get('credit_type'),
            location=validated_data['location'],
            date=datetime.utcnow().date(),
            time=datetime.utcnow().time(),
            user_id=user_id
        )

        db.session.add(transaction)
        db.session.commit()

        return transaction_schema.dump(transaction), 201
    
    def get(self, transaction_id=None):
        user_id = request.user_id

        if transaction_id:
            transaction = Transaction.query.filter_by(transaction_id=transaction_id, user_id=user_id).first()
            if not transaction:
                return {'message': 'Transaction not found'}, 404
            return transaction_schema.dump(transaction), 200

        transactions = Transaction.query.filter_by(user_id=user_id).all()
        return transaction_list_schema.dump(transactions), 200