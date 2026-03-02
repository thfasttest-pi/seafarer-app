"""Extend jobs: rank, vessel_type, salary_*, contract_months, joining_date, trading_area, experience_required_months, status, updated_at

Revision ID: 003_maritime
Revises: 002_jobs_idx
Create Date: 2025-02-21

"""
from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

revision: str = "003_maritime"
down_revision: Union[str, None] = "002_jobs_idx"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("jobs", sa.Column("updated_at", sa.DateTime(timezone=True), nullable=True))
    op.add_column("jobs", sa.Column("rank", sa.String(64), nullable=True))
    op.add_column("jobs", sa.Column("vessel_type", sa.String(64), nullable=True))
    op.add_column("jobs", sa.Column("salary_min", sa.Numeric(12, 2), nullable=True))
    op.add_column("jobs", sa.Column("salary_max", sa.Numeric(12, 2), nullable=True))
    op.add_column("jobs", sa.Column("salary_currency", sa.String(8), nullable=True))
    op.add_column("jobs", sa.Column("contract_months", sa.Integer(), nullable=True))
    op.add_column("jobs", sa.Column("joining_date", sa.Date(), nullable=True))
    op.add_column("jobs", sa.Column("trading_area", sa.String(128), nullable=True))
    op.add_column("jobs", sa.Column("experience_required_months", sa.Integer(), nullable=True))
    op.add_column(
        "jobs",
        sa.Column("status", sa.String(32), nullable=False, server_default="published"),
    )
    op.create_index("ix_jobs_rank", "jobs", ["rank"], unique=False)
    op.create_index("ix_jobs_vessel_type", "jobs", ["vessel_type"], unique=False)
    op.create_index("ix_jobs_status", "jobs", ["status"], unique=False)
    # Backfill updated_at from created_at for existing rows
    op.execute("UPDATE jobs SET updated_at = created_at WHERE updated_at IS NULL")


def downgrade() -> None:
    op.drop_index("ix_jobs_status", table_name="jobs")
    op.drop_index("ix_jobs_vessel_type", table_name="jobs")
    op.drop_index("ix_jobs_rank", table_name="jobs")
    op.drop_column("jobs", "status")
    op.drop_column("jobs", "experience_required_months")
    op.drop_column("jobs", "trading_area")
    op.drop_column("jobs", "joining_date")
    op.drop_column("jobs", "contract_months")
    op.drop_column("jobs", "salary_currency")
    op.drop_column("jobs", "salary_max")
    op.drop_column("jobs", "salary_min")
    op.drop_column("jobs", "vessel_type")
    op.drop_column("jobs", "rank")
    op.drop_column("jobs", "updated_at")
