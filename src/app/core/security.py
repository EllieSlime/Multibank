from passlib.context import CryptContext
from datetime import datetime, timedelta
from jose import jwt, JWTError
import uuid
import asyncio
from sqlalchemy.ext.asyncio import AsyncSession
from redis.asyncio import Redis

from app.core.exceptions import InvalidTokenError
from app.core.config import Config
from app.crud.crud_refresh_tokens import get_refresh_token_by_token
from app.models.refresh_tokens import RefreshToken

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def hash_password(password: str) -> str:
    """Hash password asynchronously using executor to avoid blocking event loop"""
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, pwd_context.hash, password)

async def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password asynchronously using executor to avoid blocking event loop"""
    if not plain_password or not hashed_password:
        return False
    
    try:
        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(
            None, 
            pwd_context.verify, 
            plain_password, 
            hashed_password
        )
        return bool(result)
    except Exception:
        return False

async def generate_tokens(sub):
    access_token = await generate_access(sub)
    refresh_token = await generate_refresh(sub)
    return access_token, refresh_token

async def generate_access(sub):
    exp = datetime.now()+timedelta(minutes=Config.security.access_token_expire)
    payload = {
        "sub" : str(sub),
        "exp" : exp,
        "jti" : str(uuid.uuid4())
    }
    access_token = jwt.encode(
        payload, 
        Config.security.jwt_secret_key, 
        Config.security.algorithm
        )
    return access_token
    
async def generate_refresh(sub):
    exp = datetime.now()+timedelta(days=Config.security.refresh_token_expire_days)
    payload = {
        "sub" : str(sub),
        "exp" : exp,
        "jti" : str(uuid.uuid4())
    }
    refresh_token = jwt.encode(
        payload, 
        Config.security.jwt_secret_key, 
        Config.security.algorithm
        )
    return refresh_token

async def verify_access_token(token: str, redis_conn: Redis | None = None) -> dict:
    try:
        payload = jwt.decode(
            token, 
            Config.security.jwt_secret_key, 
            algorithms=[Config.security.algorithm]
            )
        exp = payload.get("exp")
        if datetime.fromtimestamp(exp) < datetime.now():
            raise InvalidTokenError 
        if redis_conn:
            jti = payload.get("jti")
            if jti and await redis_conn.get(jti):
                raise InvalidTokenError("Token revoked")
        
        return True
    except JWTError as e:
        raise InvalidTokenError(f"Invalid token: {str(e)}")
    
async def verify_refresh_token(token: str, session: AsyncSession) -> bool:
    db_refresh_token = await get_refresh_token_by_token(session, token)
    if not db_refresh_token:
        raise InvalidTokenError
    if db_refresh_token.revoked:
        raise InvalidTokenError
    if db_refresh_token.expires_at < datetime.now():
        raise InvalidTokenError
    return True
    
async def blacklist_jti(token: str, redis_conn: Redis):
    payload = jwt.decode(token, Config.security.jwt_secret_key, algorithms=[Config.security.algorithm])
    jti = payload.get("jti")
    exp = payload.get("exp")

    if not jti or not exp:
        raise ValueError("Token missing jti or exp")
    
    expire_timestamp = datetime.fromtimestamp(exp)
    expire_seconds = int((expire_timestamp - datetime.now()).total_seconds())
    
    if expire_seconds <= 0:
        raise ValueError("Token already expired")

    await redis_conn.set(jti, "revoked", ex=expire_seconds)


    
