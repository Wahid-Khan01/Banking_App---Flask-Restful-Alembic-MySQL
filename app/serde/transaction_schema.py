from marshmallow import Schema, fields, validate

debit_type_choices = [
    "IMPS",
    "NEFT",
    "CW",
    "CDM",
    None
]
credit_type_choices = [
    "IMPS",
    "NEFT",
    "CD",
    "CDM",
    None
]

class TransactionSchema(Schema):
    transaction_id = fields.Int(dump_only=True)
    debit = fields.Float(allow_none=True, missing=None)
    credit = fields.Float(allow_none=True, missing=None)
    debit_type = fields.Str(allow_none=True, validate=validate.OneOf(debit_type_choices), missing=None)
    credit_type = fields.Str(allow_none=True, validate=validate.OneOf(credit_type_choices), missing=None)
    location = fields.Str(required=True, validate=validate.Length(max=100))
    date = fields.Date(dump_only=True)
    time = fields.Time(dump_only=True) 
    user_id = fields.Int()

transaction_schema = TransactionSchema()
transaction_list_schema = TransactionSchema(many=True)
