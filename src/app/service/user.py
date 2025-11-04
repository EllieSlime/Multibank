from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from redis.asyncio import Redis
from datetime import datetime, timedelta

from app.crud.crud_user import create_user, get_user_by_email, get_user_by_phone_number
from app.schemas.user import UserRegister, UserLogin, UserRegisterAnswer, UserLoginAnswer, UserPublic, Token, UserLogout, TokenRefresh
from app.crud.crud_refresh_tokens import create_refresh_token, get_refresh_token_by_token, get_refresh_token_by_user_id, invalidate_refresh_token

from app.core.exceptions import AuthenticationFailedError, ServiceError, InvalidTokenError
from app.core.config import Config
from app.core.logger import get_logger
from app.core.security import verify_password, hash_password, generate_tokens, blacklist_jti



class UserService:
    def __init__(self, session: AsyncSession, redis_conn: Redis | None = None):
        self.session = session
        self.redis_conn = redis_conn


    async def service_create_user(self, user: UserRegister):
        user.password = await hash_password(str(user.password))
        await create_user(self.session, user)
        
        return UserRegisterAnswer(
                email_address = user.email_address,
                phone_number = user.phone_number,
                first_name = user.first_name,
                last_name = user.last_name,
                middle_name = user.middle_name,
            )

    async def service_login_user(self, user: UserLogin):
        if "@" in user.identifier:
            db_user = await get_user_by_email(self.session, user.identifier)
        else:
            db_user = await get_user_by_phone_number(self.session, user.identifier)
        
        if not db_user:
            raise AuthenticationFailedError
        
        if not await verify_password(user.password, db_user.hashed_password):
            raise AuthenticationFailedError

        access_token, refresh_token = await generate_tokens(db_user.id)

        await create_refresh_token(self.session, refresh_token, db_user.id, datetime.now() + timedelta(days=Config.security.refresh_token_expire_days))
        return UserLoginAnswer(
            access_token = Token(
                access_token = access_token,
                token_type = "bearer"
            ),
            refresh_token= refresh_token
        )

    async def service_logout_user(self, user: UserLogout):
        """
        Logout user by blacklisting their JWT token
        """
        if not self.redis_conn:
            raise ServiceError("Redis connection not available for logout")
        
        try:
            await blacklist_jti(user.token, self.redis_conn)

            
            return {"message": "Successfully logged out"}
            
        except ValueError as e:
            raise InvalidTokenError
        except TimeoutError as e:
            raise ServiceError
        

        
        
        