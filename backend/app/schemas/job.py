"""Job schemas. All new fields optional for backward compatibility."""

from datetime import date, datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel


class JobListItem(BaseModel):
    """Job list item."""

    id: UUID
    company_id: UUID | None = None
    title: str
    description: str | None = None
    created_at: datetime
    # Extended (optional for backward compat)
    rank: str | None = None
    vessel_type: str | None = None
    salary_min: Decimal | None = None
    salary_max: Decimal | None = None
    salary_currency: str | None = None
    contract_months: int | None = None
    joining_date: date | None = None
    status: str | None = None


class JobDetail(BaseModel):
    """Job detail (GET /jobs/{id})."""

    id: UUID
    company_id: UUID | None = None
    title: str
    description: str | None = None
    created_at: datetime
    updated_at: datetime | None = None
    rank: str | None = None
    vessel_type: str | None = None
    salary_min: Decimal | None = None
    salary_max: Decimal | None = None
    salary_currency: str | None = None
    contract_months: int | None = None
    joining_date: date | None = None
    trading_area: str | None = None
    experience_required_months: int | None = None
    status: str | None = None
