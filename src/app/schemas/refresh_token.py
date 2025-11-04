from pydantic import BaseModel
from app.schemas.user import Token

class TokenRefresh(BaseModel):
    refresh_token: str

class TokenRefreshAnswer(BaseModel):
    access_token: Token
    refresh_token: str

class InvalidateTokens(BaseModel):
    access_token: Token
    refresh_token: str

class InvalidateTokensAnswer(BaseModel):
    message: str