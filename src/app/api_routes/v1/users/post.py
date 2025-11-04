from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from app.db.session import get_db
from app.schemas.user import UserRegister, UserRegisterAnswer, UserLogin, UserLoginAnswer, UserLogout, UserLogoutAnswer
from app.core.limiter import limiter
from app.core.redis_client import get_redis
from app.service.user import UserService

router = APIRouter()

@router.post("/auth/register", response_model=UserRegisterAnswer, status_code=status.HTTP_201_CREATED)
@limiter.limit("5/second")
async def register_user(
    request: Request,
    user: UserRegister,
    db: AsyncSession = Depends(get_db)
):
    service = UserService(db)
    created_user = await service.service_create_user(user)
    return created_user

@router.post("/auth/login", response_model=UserLoginAnswer)
@limiter.limit("5/second")
async def login_user(
    request: Request,
    user: UserLogin,
    db: AsyncSession = Depends(get_db)
):
    service = UserService(db)
    logged_user = await service.service_login_user(user)
    return logged_user

@router.post("/auth/logout/", response_model=UserLogoutAnswer)
@limiter.limit("5/second")
async def logout_user(
    request: Request,
    user: UserLogout,
    db: AsyncSession = Depends(get_db),
    redis_conn: Redis = Depends(get_redis)
):
    service = UserService(db, redis_conn)
    logout_result = await service.service_logout_user(user)
    return logout_result