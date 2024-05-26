from functools import wraps
from flask import request
from app.controllers.get_token import get_user_id_from_token

def get_user_info_from_token(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        token = request.cookies.get('token')
        user_id = get_user_id_from_token(token)
        request.user_id = user_id
        return func(*args, **kwargs)
    return wrapper