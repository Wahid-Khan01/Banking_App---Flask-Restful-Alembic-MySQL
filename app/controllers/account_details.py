from app.controllers.base_class import Base
from app import db
from flask import request
from app.serde.account_details_schema import account_details_schema
from app.models.user_model import User
from app.models.account_details_model import AccountDetails
import re
from marshmallow import ValidationError

class AccountDetailsBP(Base):
    def post(self, user_id):
        data = request.json
        logged_in_user_id = request.user_id
        logged_in_user = User.query.get(logged_in_user_id)
        special_characters = r"[!@#$%^&*(),.?\":{}|<>]123456789"
        
        if logged_in_user.role not in ['Admin','Staff']:
            return {'message': 'Only Admin or Staff users can change roles'}, 403


        if not data:
            return {'message':'No data Provided'}, 400
        if not data.get('account_holder_name'):
            return {'message':'Account holder name cannot be empty'}, 400
        if not data.get('account_number'):
            return {'message':'Account Number cannot be empty'}, 400
        if not data.get('ifsc_code'):
            return {'message':'IFSC code cannot be empty'}, 400
        if not data.get('branch_name'):
            return {'message':'Branch name cannot be empty'}, 400
        if not data.get('father_name'):
            return {'message':'Father name cannot be empty'}, 400
        if not data.get('address'):
            return {'message':'Address cannot be empty'}, 400
        if not data.get('mobile_number'):
            return {'message':'Mobile number cannot be empty'}, 400
        if not data.get('email'):
            return {'message':'Email cannot be empty'}, 400
        if not data.get('account_type'):
            return {'message':'Account type cannot be empty'}, 400
        if not data.get('account_number').isdigit():
            return {'message':"Account number should be numeric only"}, 400
        if not data.get('mobile_number').isdigit():
            return {'message':"Mobile number should be numeric only"}, 400
        if re.search(special_characters, data.get('account_holder_name')):
            return {'message': 'Account Holder Name should not contain special characters'}, 400
        if re.search(special_characters, data.get('father_name')):
            return {'message': 'Father Name should not contain special characters'}, 400
        if len(data.get('account_number'))<12:
            return {'message':'Check your account number there should be 12 digit in account number'}
        
        existing_account = AccountDetails.query.filter_by(account_number=data.get('account_number')).first()
        if existing_account:
            return {'message':'Account Details for given account number is already exist'}
        
        try:
            validated_data = account_details_schema.load(data)
        except ValidationError as e:
            print(e)
            return {'message':'Validation Error', 'errors':e.messages}, 400
        
        new_acc_details = AccountDetails(user_id=user_id, **validated_data)
        db.session.add(new_acc_details)
        db.session.commit()

        return {'message': 'Account details added successfully'}, 201


    def put(self, user_id):
            data = request.json
            logged_in_user_id = request.user_id
            logged_in_user = User.query.get(logged_in_user_id)
            special_characters = r"[!@#$%^&*(),.?\":{}|<>]123456789"

            if logged_in_user.role not in ['Admin', 'Staff']:
                return {'message': 'Only Admin or Staff users can update account details'}, 403

            account = AccountDetails.query.filter_by(user_id=user_id).first()
            if not account:
                return {'message': 'Account details not found'}, 404
            
            if not data:
                return {'message':'No data Provided'}, 400
            if not data.get('account_holder_name'):
                return {'message':'Account holder name cannot be empty'}, 400
            if not data.get('account_number'):
                return {'message':'Account Number cannot be empty'}, 400
            if not data.get('ifsc_code'):
                return {'message':'IFSC code cannot be empty'}, 400
            if not data.get('branch_name'):
                return {'message':'Branch name cannot be empty'}, 400
            if not data.get('father_name'):
                return {'message':'Father name cannot be empty'}, 400
            if not data.get('address'):
                return {'message':'Address cannot be empty'}, 400
            if not data.get('mobile_number'):
                return {'message':'Mobile number cannot be empty'}, 400
            if not data.get('email'):
                return {'message':'Email cannot be empty'}, 400
            if not data.get('account_type'):
                return {'message':'Account type cannot be empty'}, 400
            if not data.get('account_number').isdigit():
                return {'message':"Account number should be numeric only"}, 400
            if not data.get('mobile_number').isdigit():
                return {'message':"Mobile number should be numeric only"}, 400
            if re.search(special_characters, data.get('account_holder_name')):
                return {'message': 'Account Holder Name should not contain special characters'}, 400
            if re.search(special_characters, data.get('father_name')):
                return {'message': 'Father Name should not contain special characters'}, 400
            if len(data.get('account_number'))<12:
                return {'message':'Check your account number there should be 12 digit in account number'}
    
            try:
                validated_data = account_details_schema.load(data)
            except ValidationError as e:
                return {'message':'Validation Error', 'errors':e.messages}, 400

            for key, value in data.items():
                setattr(account, key, value)

            db.session.commit()

            return {'message': 'Account details updated successfully'}

    def delete(self, user_id):
        account = AccountDetails.query.filter_by(user_id=user_id).first()
        if not account:
            return {'message': 'Account details not found'}, 404
        db.session.delete(account)
        db.session.commit()
        return {'message': 'Account details deleted successfully'}, 200
    
    def get(self, user_id=None):
        customer_id = request.user_id

        if user_id:
            account = AccountDetails.query.filter_by(user_id=user_id).first()
            if not account:
                return {'message': 'Account details not found'}, 404
            result = account_details_schema.dump(account)
            return result, 200
        else:
            account = AccountDetails.query.filter_by(user_id=customer_id).first()
            if not account:
                return {'message': 'Account details not found'}, 404
            result = account_details_schema.dump(account)
            return result, 200
