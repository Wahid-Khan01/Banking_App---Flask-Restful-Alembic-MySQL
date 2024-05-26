from hashlib import sha256
import jwt
from app.models.user_model import User
from app.serde.user_schema import UserSchema
from datetime import datetime, timezone, timedelta
from app import secret_key
from flask import request, session, jsonify, Blueprint, make_response
from marshmallow import ValidationError

login = Blueprint('login', __name__)
@login.route('/login', methods=['POST'])
def post():

    data = request.json
    user_id_in_session = session.get('id')

    if user_id_in_session:
        if user_id_in_session == data.get('id'):
            return {'message':'you are already logged in'}, 400

    if not data:
        return {'message': 'No JSON data provided'}, 400

    email = data.get('email')
    mobile_number = data.get('mobile_number')
    password = data.get('password')

    if email and mobile_number:
        return {'message': 'Please provide either email or mobile_number, not both'}, 400

    try:
        if email:
            login_data = {'email': email, 'password': password}
        elif mobile_number:
            login_data = {'mobile_number': mobile_number, 'password': password}

        validated_data = UserSchema(only=('email', 'mobile_number', 'password')).load(login_data)
    except ValidationError as e:
        return {'message':'Validation error', 'errors': e.messages}

    if email:
        user = User.query.filter_by(email=validated_data.get('email')).first()
    elif mobile_number:
        user = User.query.filter_by(mobile_number=validated_data.get('mobile_number')).first()

    if user and sha256(validated_data['password'].encode('utf-8')).hexdigest() == user.password:
        if 'id' in session and session['id'] == user.id:
            return {'message': 'You are already logged in'}, 400
        session['id'] = user.id
        expiry = datetime.now(timezone.utc) + timedelta(minutes=60)
        payload = {'id': user.id, 'email': user.email, 'exp': expiry}
        token = jwt.encode(payload, secret_key, algorithm='HS256')
        response = make_response(jsonify({'message': 'Login Successful', 'token': token}))
        response.set_cookie('token', token, httponly=True)
        return response, 200
    else:
        return {'message': 'Invalid Credentials'}, 401