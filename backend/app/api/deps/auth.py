"""Auth dependency: initData validation + user resolution."""

from typing import Annotated

from fastapi import Depends, Header, Request
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db
from app.core.errors import AuthError
from app.core.security.init_data import Claims, verify_init_data
from app.models.user import User


async def get_current_user(
    request: Request,
    db: Annotated[AsyncSession, Depends(get_db)],
    x_tg_init_data: Annotated[str | None, Header(alias="X-Tg-Init-Data")] = None,
) -> User:
    """
    Verify initData, resolve/create user, store in request.state.
    Raises HTTPException 401 on invalid initData.
    """
    if not x_tg_init_data:
        raise AuthError("Missing X-Tg-Init-Data")

    try:
        claims = verify_init_data(x_tg_init_data)
    except ValueError as e:
        raise AuthError(str(e))

    request.state.tg_user_id = claims.user_id
    request.state.claims = claims

    result = await db.execute(
        select(User).where(User.telegram_user_id == claims.user_id)
    )
    user = result.scalar_one_or_none()
    if not user:
        user = User(telegram_user_id=claims.user_id, role="seafarer")
        db.add(user)
        await db.flush()
    request.state.user = user
    return user
