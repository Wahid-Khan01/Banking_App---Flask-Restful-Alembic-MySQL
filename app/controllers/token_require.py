from functools import wraps
from flask import request
import jwt
from app import secret_key

def token_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get('token')

        if not token:
            return {'error':'Token is missing'}, 401
        
        try:
            payload = jwt.decode(token, secret_key, algorithms=['HS256'])
            user_id = payload['id']

        except jwt.ExpiredSignatureError:
            return {'message':'Token has expired'}, 401
        except jwt.InvalidTokenError:
            return {'message':'Invalid token'}, 401
        
        return func(*args, **kwargs)
    
    return decorated_function