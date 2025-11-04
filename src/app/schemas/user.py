from __future__ import annotations

from pydantic import BaseModel, field_validator, EmailStr
from pydantic import ConfigDict

from app.core.exceptions import ValidationFailed

SPECIAL_CHARS = "!@#$%^&*()_+-=,.?"

class UserId(BaseModel):
    id: int


class UserRegister(BaseModel):
    email_address: str
    phone_number: str
    first_name: str
    last_name: str
    middle_name: str
    password: str

    @field_validator("email_address")
    def validate_email(cls, v):
        try:
            EmailStr._validate(v)
        except ValueError:
            raise ValidationFailed("Invalid email format")
        return v
    
    @field_validator("phone_number")
    def validate_phone_number(cls, v):
        if not v.isdigit():
            raise ValidationFailed("Phone number must contain only digits")
        if len(v) != 11:
            raise ValidationFailed("Phone number must be exactly 11 digits")
        return v
    
    @field_validator("password")
    def validate_password(cls, v):
        if len(v) < 8 or len(v) > 32:
            raise ValidationFailed("Password must contain at least 8 letters and be shorter than 32 symbols")
        if not any(c.isupper() for c in v):
            raise ValidationFailed("Password must contain at least one capitalized letter")
        if not any(c.isdigit() for c in v):
            raise ValidationFailed("Password must contain at least 1 digit")
        if not v.isascii():
            raise ValidationFailed("Password must be in latin")
        if not any(c in SPECIAL_CHARS for c in v):
            raise ValidationFailed("Password must contain at least one special character")
        return v

class UserRegisterAnswer(BaseModel):
    email_address: str
    phone_number: str
    first_name: str
    last_name: str
    middle_name: str

class UserLogin(BaseModel):
    identifier: str  # can be email or username
    password: str # unhashed password

    @field_validator("identifier")
    def validate_identifier(cls, v):
        if "@" in v:
            try:
                EmailStr._validate(v)
            except ValueError:
                raise ValidationFailed("Invalid email format")
        else:
            digits = "".join(filter(str.isdigit, v))
            if len(digits) != 10:
                raise ValidationFailed("Phone number must be exactly 10 digits")
        return v
    
class UserLoginAnswer(BaseModel):
    access_token: Token
    refresh_token: str

    model_config = ConfigDict(from_attributes=True)

class UserLogout(BaseModel):
    token: str

class UserLogoutAnswer(BaseModel):
    message: str

class UserCredentials(BaseModel):
    phone_number: str
    password: str


class UserPublic(UserId):
    phone_number: str
    email_address: str

    model_config = ConfigDict(from_attributes=True)


class UserInDB(UserPublic):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str
    exp: int | None = None

class TokenRefresh(BaseModel):
    refresh_token: str