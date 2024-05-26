from marshmallow import Schema, fields, validate


role_choices = [
        "Admin",
        "Customer",
        "Staff"
    ]

class UserSchema(Schema):
    id = fields.Integer(dump_only=True)
    full_name = fields.String(required=True)
    email = fields.Email()
    password = fields.String(required=True, validate=validate.Length(min=8))
    mobile_number = fields.String(validate=validate.Length(equal=10))
    role = fields.Str(validate=validate.OneOf(role_choices), missing='Customer')

user_schema = UserSchema()

users_schema = UserSchema(many=True)