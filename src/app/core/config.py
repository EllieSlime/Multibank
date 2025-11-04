from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import HttpUrl
from typing import Literal

class PSQLConfig(BaseSettings):
    dsn: str

    model_config = SettingsConfigDict(env_prefix='PSQL_', env_file=".env", extra="ignore")

class RedisConfig(BaseSettings):
    dsn: str

    model_config = SettingsConfigDict(env_prefix="REDIS_", env_file=".env", extra="ignore")

class SecurityConfig(BaseSettings):
    jwt_secret_key: str
    algorithm: str
    access_token_expire: int
    refresh_token_expire_days: int

    model_config = SettingsConfigDict(env_prefix="SECURITY_", env_file=".env", extra="ignore")


class Config:
    psql = PSQLConfig()
    redis = RedisConfig()
    security = SecurityConfig()
