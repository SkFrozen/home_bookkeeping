"""modified models user group and created models account incomes expense saving

Revision ID: a117b181306b
Revises: ab71a15e9619
Create Date: 2025-02-13 17:24:00.380619

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "a117b181306b"
down_revision: Union[str, None] = "ab71a15e9619"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "accounts",
        sa.Column("id", sa.Integer(), autoincrement=True, nullable=False),
        sa.Column("name", sa.String(length=100), nullable=False),
        sa.Column("balance", sa.Integer(), nullable=False),
        sa.Column(
            "currency",
            sa.Enum("USD", "RUB", "BYN", "EUR", name="currencyenum"),
            nullable=False,
        ),
        sa.Column("note", sa.String(), nullable=True),
        sa.Column(
            "owner_type", sa.Enum("user", "group", name="ownertypeenum"), nullable=False
        ),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("owner_id", sa.Integer(), nullable=False),
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
