from flask import Blueprint, request
from marshmallow import ValidationError
from hashlib import sha256
from app.models.user_model import User
from app.serde.user_schema import user_schema
from app import db
import re

signup = Blueprint('signup', __name__)

@signup.route('/signup', methods=['POST'])
def post():
    data = request.json
    special_characters = r"[!@#$%^&*(),.?\":{}|<>]123456789"

    if not data:
        return {'message': 'No data provided'}, 400

    if not data.get('full_name'):
        return {'message': 'Full name cannot be empty'}, 400

    try:
        validated_data = user_schema.load(data)
    except ValidationError as e:
        return {'message': 'Validation error', 'errors': e.messages}, 400

    if User.query.filter_by(email=validated_data['email']).count():
        return {'message': 'Email already registered. Kindly login to continue'}, 409

    if len(validated_data['full_name']) < 3:
        return {'message': 'Username should have more than 2 characters'}, 400

    if len(validated_data['password']) < 8:
        return {'message': 'Password must be at least 8 characters long'}, 400

    if not validated_data['mobile_number'].isdigit():
        return {'message':'Only numbers are allowed for mobile number'}

    if User.query.filter_by(mobile_number=validated_data['mobile_number']).count():
        return {'message': 'Mobile Number is already registered. Kindly login to continue'}, 409
    
    if re.search(special_characters, validated_data['full_name']):
        return {'message': 'Full name should not contain special characters'}, 400

    hashed_password = sha256(validated_data['password'].encode('utf-8')).hexdigest()

    role = validated_data.get('role', 'Customer')
    new_user = User(
        full_name=validated_data['full_name'],
        email=validated_data['email'],
        password=hashed_password,
        mobile_number=validated_data['mobile_number'],
        role=role
    )
    
    try:
        db.session.add(new_user)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return {'message': 'An error occurred while processing your request'}, 500

    return {"message":"You are Registered Successfully"}, 200
