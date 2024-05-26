"""Account_details

Revision ID: 80ad6e460acd
Revises: 822eb9d17fb5
Create Date: 2024-05-26 01:01:41.213087

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '80ad6e460acd'
down_revision: Union[str, None] = '822eb9d17fb5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None



def upgrade() -> None:
    op.create_table(
        'account_details',
        sa.Column('account_id', sa.Integer(), nullable=False),
        sa.Column('account_holder_name', sa.String(length=100), nullable=False),
        sa.Column('account_number', sa.String(length=20), nullable=False),
        sa.Column('ifsc_code', sa.String(length=20), nullable=False),
        sa.Column('branch_name', sa.String(length=100), nullable=False),
        sa.Column('father_name', sa.String(length=100), nullable=False),
        sa.Column('address', sa.String(length=200), nullable=False),
        sa.Column('mobile_number', sa.String(length=20), nullable=False),
        sa.Column('email', sa.String(length=120), nullable=False),
        sa.Column('date_of_birth', sa.Date(), nullable=False),
        sa.Column('balance', sa.Float(), nullable=False),
        sa.Column('nominee', sa.String(length=100), nullable=True),
        sa.Column('pan_linked', sa.Boolean(), nullable=False),
        sa.Column('account_type', sa.String(length=20), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
        sa.PrimaryKeyConstraint('account_id'),
        sa.UniqueConstraint('account_number')
    )


def downgrade() -> None:
    op.drop_table('account_details')
