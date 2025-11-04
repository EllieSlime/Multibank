from fastapi import Request
from redis.asyncio import Redis

from app.core.config import Config

redis_client = None

async def init_redis():
    global redis_client
    redis_client = await Redis.from_url(
        Config.redis.dsn,
        decode_responses=True
    )
    return redis_client

async def close_redis():
    if redis_client:
        await redis_client.close()

async def get_redis(request: Request) -> Redis:
    return request.app.state.redis