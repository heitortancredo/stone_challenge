"""Initial migration - create database

Revision ID: 31aa7d3383c0
Revises:
Create Date: 2023-12-19 21:21:37.027756

"""
# mypy: ignore-errors
from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "31aa7d3383c0"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:  # type: ignore
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "stock_quotes",
        sa.Column(
            "id", sa.BigInteger().with_variant(sa.INTEGER(), "sqlite"), autoincrement=True, nullable=False
        ),  # noqa
        sa.Column("ticker", sa.String(length=128), nullable=False),
        sa.Column("hora_fechamento", sa.String(length=128), nullable=False),
        sa.Column("preco_negocio", sa.Float(), nullable=False),
        sa.Column("quantidade_negociada", sa.Integer(), nullable=False),
        sa.Column("data_negocio", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("data_negocio", "stock_quotes", ["data_negocio"], unique=False)
    op.create_index("ticker", "stock_quotes", ["ticker"], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index("ticker", table_name="stock_quotes")
    op.drop_index("data_negocio", table_name="stock_quotes")
    op.drop_table("stock_quotes")
    # ### end Alembic commands ###
