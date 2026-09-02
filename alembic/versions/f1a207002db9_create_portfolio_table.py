"""create_portfolio_table

Revision ID: f1a207002db9
Revises: 3004a631c566
Create Date: 2026-09-02 18:42:05.335086

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'f1a207002db9'
down_revision: Union[str, Sequence[str], None] = '3004a631c566'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table('portfolios',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.String(length=255), nullable=True),
        sa.Column('currency', sa.String(length=10), nullable=False),
        sa.Column('is_default', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.func.now(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_portfolios_id'), 'portfolios', ['id'], unique=False)
    op.create_index(op.f('ix_portfolios_user_id'), 'portfolios', ['user_id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_portfolios_user_id'), table_name='portfolios')
    op.drop_index(op.f('ix_portfolios_id'), table_name='portfolios')
    op.drop_table('portfolios')
