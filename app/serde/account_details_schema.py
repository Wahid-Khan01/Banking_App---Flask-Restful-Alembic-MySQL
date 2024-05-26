from marshmallow import Schema, fields, validate
from datetime import date


type_choices = [
    "Savings",
    "Current",
]

class AccountDetailsSchema(Schema):
    account_id = fields.Int(dump_only=True)
    account_holder_name = fields.Str(required=True)
    account_number = fields.Str(required=True, validate=validate.Length(max=12))
    ifsc_code = fields.Str(required=True, validate=validate.Length(max=20))
    branch_name = fields.Str(required=True)
    father_name = fields.Str(required=True)
    address = fields.Str(required=True)
    mobile_number = fields.Str(required=True, validate=validate.Length(max=10))
    email = fields.Email(required=True)
    date_of_birth = fields.Date(required=True)
    balance = fields.Float(required=True)
    nominee = fields.Str()
    pan_linked = fields.Bool(default=False)
    account_type = fields.Str(required=True, validate=validate.OneOf(type_choices))
    user_id = fields.Int()

account_details_schema = AccountDetailsSchema()
accounts_details_schema = AccountDetailsSchema(many=True)
