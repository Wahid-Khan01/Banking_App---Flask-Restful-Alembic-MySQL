from datetime import datetime, timedelta
from app.controllers.base_class import Base
from flask import request
from app.models.transaction_model import Transaction
from app.serde.transaction_schema import transaction_list_schema

class TransactionWithDaysAPI(Base):
    
    def get(self, days=None):
        user_id = request.user_id
        current_date = datetime.utcnow().date()

        if days:
            try:
                days = int(days)
            except ValueError:
                return {'message': 'Invalid number of days'}, 400
            
            if days <= 0:
                return {'message': 'Number of days must be a positive integer'}, 400

            start_date = current_date - timedelta(days=days)

            transactions = Transaction.query.filter(
                Transaction.user_id == user_id,
                Transaction.date >= start_date,
                Transaction.date <= current_date
            ).all()
        else:
            transactions = Transaction.query.filter_by(user_id=user_id).all()

        if not transactions:
            return {'message': 'No transactions found'}, 404
        
        return transaction_list_schema.dump(transactions), 200
