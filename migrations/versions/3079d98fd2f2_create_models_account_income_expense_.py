"""create models account, income, expense, saving

Revision ID: 3079d98fd2f2
Revises: ab71a15e9619
Create Date: 2025-02-24 20:03:53.004142

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = "3079d98fd2f2"
down_revision: Union[str, None] = "ab71a15e9619"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    sa.Enum(
        "car",
        "clothes",
        "entertainment",
        "food",
        "footwear",
        "furniture",
        "househoold_goods",
        "medicine",
        "regular_payments",
        "services",
        "transport",
        "utilities",
        name="expensecategoryenum",
    ).create(op.get_bind())
    sa.Enum(
        "inheritance",
        "insurance",
        "lottery",
        "pension",
        "present",
        "rent",
        "salary",
        "sold_property",
        name="incomecategoryenum",
    ).create(op.get_bind())
    sa.Enum("USD", "RUB", "BYN", "EUR", name="currencyenum").create(op.get_bind())
    op.create_table(
        "accounts",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("balance", sa.Integer(), nullable=False),
        sa.Column(
            "currency",
            postgresql.ENUM(
                "USD", "RUB", "BYN", "EUR", name="currencyenum", create_type=False
            ),
            nullable=False,
        ),
        sa.Column("note", sa.String(), nullable=True),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("user_id", sa.Integer(), nullable=True),
        sa.Column("group_id", sa.Integer(), nullable=True),
        sa.CheckConstraint(
            "(user_id IS NOT NULL AND group_id IS NULL) OR (user_id IS NULL AND group_id IS NOT NULL)",
            name=op.f("ck__accounts__account_owner"),
        ),
        sa.ForeignKeyConstraint(
            ["group_id"],
            ["groups.id"],
            name=op.f("fk__accounts__group_id__groups"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["users.id"],
            name=op.f("fk__accounts__user_id__users"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__accounts")),
    )
    op.create_table(
        "expenses",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("amount", sa.Integer(), nullable=False),
        sa.Column(
            "date", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "category",
            postgresql.ENUM(
                "car",
                "clothes",
                "entertainment",
                "food",
                "footwear",
                "furniture",
                "househoold_goods",
                "medicine",
                "regular_payments",
                "services",
                "transport",
                "utilities",
                name="expensecategoryenum",
                create_type=False,
            ),
            nullable=False,
        ),
        sa.Column("note", sa.String(), nullable=True),
        sa.Column("account_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["account_id"],
            ["accounts.id"],
            name=op.f("fk__expenses__account_id__accounts"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__expenses")),
    )
    op.create_table(
        "incomes",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("amount", sa.Integer(), nullable=False),
        sa.Column(
            "date", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "category",
            postgresql.ENUM(
                "inheritance",
                "insurance",
                "lottery",
                "pension",
                "present",
                "rent",
                "salary",
                "sold_property",
                name="incomecategoryenum",
                create_type=False,
            ),
            nullable=False,
        ),
        sa.Column("note", sa.String(), nullable=True),
        sa.Column("account_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["account_id"],
            ["accounts.id"],
            name=op.f("fk__incomes__account_id__accounts"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__incomes")),
    )
    op.create_table(
        "savings",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("target_amount", sa.Integer(), nullable=False),
        sa.Column("current_amount", sa.Integer(), nullable=False),
        sa.Column(
            "date", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column(
            "category",
            postgresql.ENUM(
                "car",
                "clothes",
                "entertainment",
                "food",
                "footwear",
                "furniture",
                "househoold_goods",
                "medicine",
                "regular_payments",
                "services",
                "transport",
                "utilities",
                name="expensecategoryenum",
                create_type=False,
            ),
            nullable=False,
        ),
        sa.Column("periodicity", sa.String(), nullable=True),
        sa.Column("note", sa.String(), nullable=False),
        sa.Column("account_id", sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(
            ["account_id"],
            ["accounts.id"],
            name=op.f("fk__savings__account_id__accounts"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id", name=op.f("pk__savings")),
    )
    op.add_column("groups", sa.Column("note", sa.String(), nullable=True))


def downgrade() -> None:
    op.drop_column("groups", "note")
    op.drop_table("savings")
    op.drop_table("incomes")
    op.drop_table("expenses")
    op.drop_table("accounts")
    sa.Enum("USD", "RUB", "BYN", "EUR", name="currencyenum").drop(op.get_bind())
    sa.Enum(
        "inheritance",
        "insurance",
        "lottery",
        "pension",
        "present",
        "rent",
        "salary",
        "sold_property",
        name="incomecategoryenum",
    ).drop(op.get_bind())
    sa.Enum(
        "car",
        "clothes",
        "entertainment",
        "food",
        "footwear",
        "furniture",
        "househoold_goods",
        "medicine",
        "regular_payments",
        "services",
        "transport",
        "utilities",
        name="expensecategoryenum",
    ).drop(op.get_bind())
