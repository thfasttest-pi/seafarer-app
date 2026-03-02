"""Job search with keyset pagination and filters."""

from datetime import datetime
from decimal import Decimal
from uuid import UUID

from sqlalchemy import and_, desc, or_, select, tuple_
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.pagination import decode_cursor, encode_cursor
from app.models.job import Job


class JobFilters:
    """Query params for list jobs."""

    def __init__(
        self,
        rank: str | None = None,
        vessel_type: str | None = None,
        salary_min: int | Decimal | None = None,
        salary_max: int | Decimal | None = None,
        search: str | None = None,
        status: str | None = "published",
    ):
        self.rank = rank
        self.vessel_type = vessel_type
        self.salary_min = salary_min
        self.salary_max = salary_max
        self.search = search and search.strip() or None
        self.status = status


def _build_list_conditions(filters: JobFilters):
    """Build WHERE conditions for list query (deleted_at + filters)."""
    conditions = [Job.deleted_at.is_(None)]
    if filters.rank is not None:
        conditions.append(Job.rank == filters.rank)
    if filters.vessel_type is not None:
        conditions.append(Job.vessel_type == filters.vessel_type)
    if filters.salary_min is not None:
        conditions.append(Job.salary_max >= filters.salary_min)
    if filters.salary_max is not None:
        conditions.append(Job.salary_min <= filters.salary_max)
    if filters.status is not None:
        conditions.append(Job.status == filters.status)
    return conditions


async def get_job_by_id(
    db: AsyncSession,
    job_id: UUID,
) -> Job | None:
    """Get job by id. Returns None if not found or soft-deleted."""
    result = await db.execute(
        select(Job).where(
            Job.id == job_id,
            Job.deleted_at.is_(None),
        )
    )
    return result.scalar_one_or_none()


async def list_jobs_keyset(
    db: AsyncSession,
    *,
    limit: int,
    cursor: str | None = None,
    filters: JobFilters | None = None,
) -> tuple[list[Job], str | None]:
    """
    Keyset pagination with optional filters.
    ORDER BY created_at DESC, id DESC
    WHERE deleted_at IS NULL + filters. status default 'published'.
    """
    f = filters or JobFilters()
    conditions = _build_list_conditions(f)
    q = (
        select(Job)
        .where(and_(*conditions))
        .order_by(desc(Job.created_at), desc(Job.id))
    )
    if f.search:
        pattern = f"%{f.search}%"
        q = q.where(
            or_(
                Job.title.ilike(pattern),
                Job.description.ilike(pattern),
            )
        )
    if cursor:
        parsed = decode_cursor(cursor)
        if parsed:
            ts, id_str = parsed
            try:
                uid = UUID(id_str)
                q = q.where(
                    tuple_(Job.created_at, Job.id) < tuple_(ts, uid)
                )
            except (ValueError, TypeError):
                pass
    q = q.limit(limit + 1)
    result = await db.execute(q)
    rows = list(result.scalars().all())
    next_cursor = None
    if len(rows) > limit:
        rows = rows[:limit]
        last = rows[-1]
        next_cursor = encode_cursor(last.created_at, str(last.id))
    return rows, next_cursor
