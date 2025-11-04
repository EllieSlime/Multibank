from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis
from datetime import datetime
from datetime import timedelta

from app.crud.crud_refresh_tokens import create_refresh_token, get_refresh_token_by_token, get_refresh_token_by_user_id, invalidate_refresh_token
from app.core.db_exceptions_wrapper import handle_db_errors
from app.core.exceptions import ServiceError, InvalidTokenError
from app.core.logger import get_logger
from app.core.security import verify_refresh_token, generate_tokens, blacklist_jti
from app.schemas.refresh_token import TokenRefreshAnswer, Token
from app.core.config import Config

class RefreshTokenService:
    def __init__(self, session: AsyncSession, redis_conn: Redis):
        self.session = session
        self.redis_conn = redis_conn

    async def service_refresh_token(self, refresh_token: str):
        if not self.redis_conn:
            raise ServiceError("Redis connection not available for refreshing")
        
        # Verify token (raises InvalidTokenError if invalid)
        await verify_refresh_token(refresh_token, self.session)
        
        # Get token and invalidate it
        db_refresh_token = await get_refresh_token_by_token(self.session, refresh_token)
        await invalidate_refresh_token(self.session, db_refresh_token)

        # Generate new tokens
        user_id = db_refresh_token.user_id
        access_token, refresh_token = await generate_tokens(user_id)

        # Revoke refresh and access tokens
        await create_refresh_token(self.session, refresh_token, user_id, datetime.now() + timedelta(days=Config.security.refresh_token_expire_days))
        await blacklist_jti(access_token, self.redis_conn)

        return TokenRefreshAnswer(
            access_token = Token(
                access_token = access_token,
                token_type = "bearer"
            ),
            refresh_token = refresh_token
        )
