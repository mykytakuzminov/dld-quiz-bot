"""create initial tables

Revision ID: 0627b8ad4ba2
Revises:
Create Date: 2026-04-22 14:07:02.076145

"""

from collections.abc import Sequence

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "0627b8ad4ba2"
down_revision: str | Sequence[str] | None = None
branch_labels: str | Sequence[str] | None = None
depends_on: str | Sequence[str] | None = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        "questions",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column("text", sa.Text(), nullable=False),
        sa.Column("options", sa.JSON(), nullable=False),
        sa.Column("correct_answer", sa.Text(), nullable=False),
        sa.Column("topic", sa.String(20), nullable=False, index=True),
        sa.Column("land", sa.String(50), nullable=True, index=True),
    )

    op.create_table(
        "users",
        sa.Column("telegram_id", sa.BigInteger(), primary_key=True, nullable=False),
        sa.Column("username", sa.String(32)),
        sa.Column("selected_land", sa.String(50), nullable=False),
        sa.Column(
            "created_at", sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False
        ),
    )

    op.create_table(
        "exam_sessions",
        sa.Column("id", sa.Integer(), primary_key=True, autoincrement=True, nullable=False),
        sa.Column("user_id", sa.BigInteger(), nullable=False),
        sa.Column("total_questions", sa.Integer(), server_default="33", nullable=False),
        sa.Column("correct_answers", sa.Integer(), server_default="0", nullable=False),
        sa.Column(
            "created_at", sa.TIMESTAMP(timezone=True), server_default=sa.func.now(), nullable=False
        ),
        sa.ForeignKeyConstraint(["user_id"], ["users.telegram_id"], ondelete="CASCADE"),
    )


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_table("exam_sessions")
    op.drop_table("users")
    op.drop_table("questions")
