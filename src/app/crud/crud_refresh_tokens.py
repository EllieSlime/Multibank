from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from datetime import datetime
from typing import Union

from app.models.refresh_tokens import RefreshToken
from app.core.db_exceptions_wrapper import handle_db_errors


@handle_db_errors
async def create_refresh_token(
    session: AsyncSession, 
    refresh_token: str, 
    user_id: int, 
    expires_at: datetime
):
    db_refresh_token = RefreshToken(
        refresh_token=refresh_token,
        user_id=user_id,
        expires_at=expires_at
    )
    session.add(db_refresh_token)
    await session.commit()
    await session.refresh(db_refresh_token)
    return db_refresh_token

@handle_db_errors
async def get_refresh_token_by_token(
    session: AsyncSession, 
    token: Union[str, RefreshToken]
):
    # Allow passing either raw token string or model instance
    token_value = token.refresh_token if isinstance(token, RefreshToken) else token
    result = await session.execute(
        select(RefreshToken).where(RefreshToken.refresh_token == token_value)
    )
    return result.scalar_one_or_none()

@handle_db_errors
async def get_refresh_token_by_user_id(
    session: AsyncSession, 
    user_id: int
):
    result = await session.execute(
        select(RefreshToken).where(RefreshToken.user_id == user_id)
    )
    return result.scalar_one_or_none()

@handle_db_errors
async def invalidate_refresh_token(
    session: AsyncSession, 
    token: Union[str, RefreshToken]
):
    token_value = token.refresh_token if isinstance(token, RefreshToken) else token
    result = await session.execute(
        update(RefreshToken).where(RefreshToken.refresh_token == token_value).values(revoked=True)
    )
    await session.commit()
    return result.rowcount > 0