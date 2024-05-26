from flask import request
from flask_mail import Message
from app import mail
from datetime import datetime, timedelta
from app.controllers.base_class import Base
from app.models.user_model import User
from app.models.transaction_model import Transaction
from app.serde.transaction_schema import transaction_schema

class MailRequestAPI(Base):
    def post(self):
        data = request.json
        email = data.get('email')
        days = data.get('days')

        if not email:
            return {'message': 'Email address is required'}, 400

        user = User.query.filter_by(email=email).first()
        if not user:
            return {'message': 'User not found'}, 404

        if days:
            try:
                days = int(days)
            except ValueError:
                return {'message': 'Invalid number of days'}, 400
                
            if days <= 0:
                return {'message': 'Number of days must be a positive integer'}, 400

            current_date = datetime.utcnow().date()
            start_date = current_date - timedelta(days=days)
            transactions = Transaction.query.filter(
                Transaction.user_id == user.id,
                Transaction.date >= start_date,
                Transaction.date <= current_date
            ).all()
        else:
            transactions = Transaction.query.filter_by(user_id=user.id).all()

        if not transactions:
            return {'message': 'No transactions found'}, 404

        formatted_transactions = [transaction_schema.dump(transaction) for transaction in transactions]

        msg = Message('Transaction Data', recipients=[email])
        msg.body = f'Transaction Data: {formatted_transactions}'

        try:
            mail.send(msg)
            return {'message': 'Email sent successfully'}, 200
        except Exception as e:
            return {'message': str(e)}, 500

