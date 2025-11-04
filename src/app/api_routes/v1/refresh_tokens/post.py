from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from app.db.session import get_db
from app.schemas.refresh_token import TokenRefreshAnswer, TokenRefresh
from app.core.limiter import limiter
from app.core.redis_client import get_redis
from app.service.refresh_token import RefreshTokenService

router = APIRouter()

@router.post("/auth/refresh", response_model=TokenRefreshAnswer)
@limiter.limit("5/second")
async def refresh_token(
    request: Request,
    refresh_token: TokenRefresh,
    db: AsyncSession = Depends(get_db),
    redis_conn: Redis = Depends(get_redis)
):
    service = RefreshTokenService(session=db, redis_conn=redis_conn)
    return await service.service_refresh_token(refresh_token.refresh_token)