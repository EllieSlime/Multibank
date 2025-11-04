# * `POST /api/v1/auth/register` — Регистрация нового пользователя
# * `POST /api/v1/auth/login` — Авторизация пользователя, получение JWT токена
# * `POST /api/v1/auth/logout` — Выход из системы, инвалидирование токена
# * `POST /api/v1/auth/refresh` — Обновить токен доступа по refresh-токену

# * `GET /api/v1/auth/me` — Получить информацию о текущем пользователе (по JWT)

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

from app.schemas.user import UserRegister
from app.models.user import User
from app.core.db_exceptions_wrapper import handle_db_errors



# POST /api/v1/auth/register
@handle_db_errors
async def create_user(session: AsyncSession, user:UserRegister):
    db_user = User(
        first_name=user.first_name,
        last_name=user.last_name,
        email_address=user.email_address,
        phone_number=user.phone_number,
        hashed_password=user.password # Hashed in service layer already
    )
    session.add(db_user)
    await session.commit()
    await session.refresh(db_user)
    return db_user

@handle_db_errors
async def get_user_by_email(db: AsyncSession, email: str):
    result = await db.execute(
        select(User).where(User.email_address == email)
    )
    return result.scalar_one_or_none()

@handle_db_errors
async def get_user_by_phone_number(db: AsyncSession, phone_number: str):
    result = await db.execute(
        select(User).where(User.phone_number == phone_number)
    )
    return result.scalar_one_or_none()

@handle_db_errors
async def get_user_by_id(db: AsyncSession, id: int):
    result = await db.execute(
        select(User).where(User.id == id)
    )
    return result.scalar_one_or_none()