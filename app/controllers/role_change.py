from flask import request
from app.models.user_model import User
from app.controllers.base_class import Base
from app import db


class Role_Change(Base):
    def get(self, user_id):
        logged_in_user_id = request.user_id
        logged_in_user = User.query.get(logged_in_user_id)
        if logged_in_user.role != 'Admin':
            return {'message': 'Only Admin users can change roles'}, 403

        user_to_update = User.query.get(user_id)
        if not user_to_update:
            return {'message': 'User not found'}, 404
        
        new_role = request.json.get('role')
        if not new_role:
            return {"message":"No data provided"}

        if new_role not in ['Customer', 'Staff']:
            return {'message': 'Invalid role , Kindly select in between Customer and Staff'}, 400
        
        user_to_update.role = new_role
        db.session.commit()
        
        return {'message': 'User role updated successfully'}, 200


