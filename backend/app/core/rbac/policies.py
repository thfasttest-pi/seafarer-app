"""RBAC policy layer. Use these instead of inline role checks."""

from typing import Any
from uuid import UUID

from app.core.errors import ForbiddenError


def authorize_super_admin(user: Any) -> None:
    """Raise ForbiddenError if user is not super_admin."""
    if getattr(user, "role", None) != "super_admin":
        raise ForbiddenError("Super admin access required")


def authorize_company_access(user: Any, company_id: UUID) -> None:
    """Raise ForbiddenError if user cannot access company (own or super_admin)."""
    role = getattr(user, "role", None)
    if role == "super_admin":
        return
    user_company = getattr(user, "company_id", None)
    if user_company != company_id:
        raise ForbiddenError("Access denied to this company")


def authorize_job_edit(user: Any, job: Any) -> None:
    """Raise ForbiddenError if user cannot edit job (own company or super_admin)."""
    role = getattr(user, "role", None)
    if role == "super_admin":
        return
    if role != "company_admin":
        raise ForbiddenError("Company admin access required")
    job_company = getattr(job, "company_id", None)
    user_company = getattr(user, "company_id", None)
    if job_company != user_company:
        raise ForbiddenError("Cannot edit jobs of other companies")
