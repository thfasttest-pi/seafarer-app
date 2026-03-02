"""Current user: GET /api/v1/me."""

from typing import Annotated

from fastapi import APIRouter, Depends

from app.api.deps.auth import get_current_user
from app.models.user import User
from app.schemas.user import MeResponse

router = APIRouter(prefix="/me", tags=["me"])


@router.get("", response_model=MeResponse)
async def get_me(user: Annotated[User, Depends(get_current_user)]) -> MeResponse:
    """
    Current user (find-or-create by initData already done in get_current_user).
    """
    return MeResponse(
        id=user.id,
        telegram_id=user.telegram_user_id,
        role=user.role,
        created_at=user.created_at,
    )
