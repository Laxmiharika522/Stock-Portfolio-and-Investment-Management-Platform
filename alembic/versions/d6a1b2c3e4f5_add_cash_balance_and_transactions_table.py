"""add_cash_balance_and_transactions_table

Revision ID: d6a1b2c3e4f5
Revises: 7a892b104c21
Create Date: 2026-09-08 16:10:00.000000

Day 6: Adds cash_balance and total_invested columns to portfolios table.
       Creates transactions table for BUY/SELL trade records.
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd6a1b2c3e4f5'
down_revision: Union[str, Sequence[str], None] = '7a892b104c21'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: add portfolio balance fields and create transactions table."""

    # ── 1. Add cash_balance and total_invested to portfolios ──────────────────
    op.add_column(
        'portfolios',
        sa.Column('cash_balance', sa.Float(), nullable=False, server_default='0.0')
    )
    op.add_column(
        'portfolios',
        sa.Column('total_invested', sa.Float(), nullable=False, server_default='0.0')
    )

    # ── 2. Create transactions table ──────────────────────────────────────────
    op.create_table(
        'transactions',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('portfolio_id', sa.UUID(), nullable=False),
        sa.Column('stock_id', sa.UUID(), nullable=False),
        sa.Column(
            'transaction_type',
            sa.Enum('BUY', 'SELL', name='transactiontype'),
            nullable=False,
        ),
        sa.Column('quantity', sa.Float(), nullable=False),
        sa.Column('price_per_share', sa.Float(), nullable=False),
        sa.Column('fees', sa.Float(), nullable=False, server_default='0.0'),
        sa.Column('total_amount', sa.Float(), nullable=False),
        sa.Column('notes', sa.Text(), nullable=True),
        sa.Column(
            'transacted_at',
            sa.DateTime(timezone=True),
            nullable=False,
            server_default=sa.func.now(),
        ),
        sa.Column(
            'created_at',
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            'updated_at',
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.ForeignKeyConstraint(
            ['portfolio_id'], ['portfolios.id'], ondelete='CASCADE'
        ),
        sa.ForeignKeyConstraint(
            ['stock_id'], ['stocks.id'], ondelete='CASCADE'
        ),
        sa.PrimaryKeyConstraint('id'),
    )

    # ── 3. Create indexes ─────────────────────────────────────────────────────
    op.create_index(op.f('ix_transactions_id'), 'transactions', ['id'], unique=False)
    op.create_index(op.f('ix_transactions_portfolio_id'), 'transactions', ['portfolio_id'], unique=False)
    op.create_index(op.f('ix_transactions_stock_id'), 'transactions', ['stock_id'], unique=False)
    op.create_index(op.f('ix_transactions_transaction_type'), 'transactions', ['transaction_type'], unique=False)
    op.create_index(op.f('ix_transactions_transacted_at'), 'transactions', ['transacted_at'], unique=False)


def downgrade() -> None:
    """Downgrade schema: remove transactions table and portfolio balance columns."""

    # Drop indexes first
    op.drop_index(op.f('ix_transactions_transacted_at'), table_name='transactions')
    op.drop_index(op.f('ix_transactions_transaction_type'), table_name='transactions')
    op.drop_index(op.f('ix_transactions_stock_id'), table_name='transactions')
    op.drop_index(op.f('ix_transactions_portfolio_id'), table_name='transactions')
    op.drop_index(op.f('ix_transactions_id'), table_name='transactions')

    # Drop transactions table (enum is auto-dropped for SQLite; PostgreSQL needs explicit drop)
    op.drop_table('transactions')

    # Remove balance columns from portfolios
    op.drop_column('portfolios', 'total_invested')
    op.drop_column('portfolios', 'cash_balance')
