from flask import request
from app.models.user_model import User
from app.models.account_details_model import AccountDetails
from app.serde.account_details_schema import accounts_details_schema
from app.controllers.base_class import Base


class BankerAccountAPI(Base):
    def get(self, user_id=None):
        logged_in_user_id = request.user_id
        logged_in_user = User.query.get(logged_in_user_id)
        if not logged_in_user:
            return {'message': 'User not found'}, 404
        if logged_in_user.role not in ['Admin', 'Staff']:
            return {'message': 'Unauthorized access'}, 403

        if user_id:
            account_details = AccountDetails.query.filter_by(user_id=user_id).all()
            return {
                'user_id': user_id,
                'account_details': accounts_details_schema.dump(account_details)
            }, 200
        else:
            all_account_details = AccountDetails.query.all()
            return {
                'account_details': accounts_details_schema.dump(all_account_details)
            }, 200
        
