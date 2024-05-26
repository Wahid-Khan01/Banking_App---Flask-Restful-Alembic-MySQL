from flask_restful import Resource
from app.controllers.token_require import token_required
from app.controllers.get_user_info_from_token import get_user_info_from_token



class Base(Resource):
    decorators = [token_required, get_user_info_from_token]