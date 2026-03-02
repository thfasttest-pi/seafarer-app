"""Jobs API: list (keyset + filters) and detail."""

from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, Query

from app.api.deps.auth import get_current_user
from app.api.deps.rate_limit import require_rate_limit, RateLimitTier
from app.core.constants import MAX_LIMIT
from app.core.db import get_db
from app.core.errors import NotFoundError
from app.core.pagination import clamp_limit
from app.models.user import User
from app.schemas.job import JobDetail, JobListItem
from app.schemas.pagination import Page
from app.services.job_search import JobFilters, get_job_by_id, list_jobs_keyset
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/jobs", tags=["jobs"])


def _job_to_list_item(r) -> JobListItem:
    return JobListItem(
        id=r.id,
        company_id=r.company_id,
        title=r.title,
        description=r.description,
        created_at=r.created_at,
        rank=getattr(r, "rank", None),
        vessel_type=getattr(r, "vessel_type", None),
        salary_min=getattr(r, "salary_min", None),
        salary_max=getattr(r, "salary_max", None),
        salary_currency=getattr(r, "salary_currency", None),
        contract_months=getattr(r, "contract_months", None),
        joining_date=getattr(r, "joining_date", None),
        status=getattr(r, "status", None),
    )


def _job_to_detail(r) -> JobDetail:
    return JobDetail(
        id=r.id,
        company_id=r.company_id,
        title=r.title,
        description=r.description,
        created_at=r.created_at,
        updated_at=getattr(r, "updated_at", None),
        rank=getattr(r, "rank", None),
        vessel_type=getattr(r, "vessel_type", None),
        salary_min=getattr(r, "salary_min", None),
        salary_max=getattr(r, "salary_max", None),
        salary_currency=getattr(r, "salary_currency", None),
        contract_months=getattr(r, "contract_months", None),
        joining_date=getattr(r, "joining_date", None),
        trading_area=getattr(r, "trading_area", None),
        experience_required_months=getattr(r, "experience_required_months", None),
        status=getattr(r, "status", None),
    )


@router.get("", response_model=Page[JobListItem])
async def list_jobs(
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
    _: Annotated[None, Depends(require_rate_limit(RateLimitTier.SEARCH))],
    limit: Annotated[int | None, Query(ge=1, le=MAX_LIMIT)] = 20,
    cursor: Annotated[str | None, Query()] = None,
    rank: Annotated[str | None, Query()] = None,
    vessel_type: Annotated[str | None, Query()] = None,
    salary_min: Annotated[int | None, Query(ge=0)] = None,
    salary_max: Annotated[int | None, Query(ge=0)] = None,
    search: Annotated[str | None, Query()] = None,
    status: Annotated[str | None, Query(description="draft | published | closed")] = None,
) -> Page[JobListItem]:
    """
    List jobs with keyset pagination and filters.
    Default status=published when not provided. Use cursor for next page.
    """
    limit = clamp_limit(limit)
    effective_status = (status or "").strip() or "published"
    filters = JobFilters(
        rank=rank,
        vessel_type=vessel_type,
        salary_min=salary_min,
        salary_max=salary_max,
        search=search,
        status=effective_status,
    )
    rows, next_cursor = await list_jobs_keyset(
        db, limit=limit, cursor=cursor, filters=filters
    )
    items = [_job_to_list_item(r) for r in rows]
    return Page(items=items, next_cursor=next_cursor)


@router.get("/{job_id}", response_model=JobDetail)
async def get_job(
    db: Annotated[AsyncSession, Depends(get_db)],
    user: Annotated[User, Depends(get_current_user)],
    job_id: UUID,
) -> JobDetail:
    """Job detail. 404 if not found or soft-deleted."""
    job = await get_job_by_id(db, job_id)
    if job is None:
        raise NotFoundError("Job not found")
    return _job_to_detail(job)
