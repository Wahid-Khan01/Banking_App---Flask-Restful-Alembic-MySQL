"""Transaction

Revision ID: b5753b296762
Revises: 80ad6e460acd
Create Date: 2024-05-26 08:47:44.986910

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b5753b296762'
down_revision: Union[str, None] = '80ad6e460acd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        'transaction',
        sa.Column('transaction_id', sa.Integer, primary_key=True, autoincrement=True),
        sa.Column('debit', sa.Float, nullable=True),
        sa.Column('credit', sa.Float, nullable=True),
        sa.Column('debit_type', sa.String(10), nullable=True),
        sa.Column('credit_type', sa.String(10), nullable=True),
        sa.Column('location', sa.String(100), nullable=False),
        sa.Column('date', sa.Date(100), nullable=False),
        sa.Column('time', sa.Time(100), nullable=False),
        sa.Column('user_id', sa.Integer, sa.ForeignKey('user.id'), nullable=False)
    )


def downgrade():
    op.drop_table('transaction')



'''
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
    balance = fields.Float(required=True)
    user_id = fields.Int(required=True)

transaction_schema = TransactionSchema()
transaction_list_schema = TransactionSchema(many=True)




mujhe ab api banana hai jo kya karega ki jab debit me kuch input aaye toh credit or credit type ko bydefault none kardega or jitna paisa debit hua hai utna balance me se debit hojayega
waise hi jab credit me koi input hoga toh debit or debit type ko by default none kardega or balance me utna credited amount add kardega'''