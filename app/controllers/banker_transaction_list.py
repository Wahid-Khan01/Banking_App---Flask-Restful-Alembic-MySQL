from flask import request
from app.models.user_model import User
from app.models.transaction_model import Transaction
from app.serde.transaction_schema import transaction_list_schema
from app.controllers.base_class import Base


class BankerTransactionAPI(Base):
    
    def get(self, user_id=None):
        logged_in_user_id = request.user_id
        logged_in_user = User.query.get(logged_in_user_id)
        if not logged_in_user:
            return {'message': 'User not found'}, 404
        if logged_in_user.role not in ['Admin', 'Staff']:
            return {'message': 'Unauthorized access'}, 403

        if user_id:
            transactions = Transaction.query.filter_by(user_id=user_id).all()
            return {
                'user_id': user_id,
                'transactions': transaction_list_schema.dump(transactions)
            }, 200
        else:
            all_transactions = Transaction.query.all()
            return {
                'transactions': transaction_list_schema.dump(all_transactions)
            }, 200