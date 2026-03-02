"""Add keyset pagination index on jobs: (created_at DESC, id DESC) WHERE deleted_at IS NULL

Revision ID: 002_jobs_idx
Revises: 001_init
Create Date: 2025-02-21

"""
from typing import Sequence, Union

from alembic import op

revision: str = "002_jobs_idx"
down_revision: Union[str, None] = "001_init"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute(
        """
        CREATE INDEX ix_jobs_keyset_pagination
        ON jobs (created_at DESC, id DESC)
        WHERE deleted_at IS NULL
        """
    )


def downgrade() -> None:
    op.drop_index("ix_jobs_keyset_pagination", table_name="jobs")
