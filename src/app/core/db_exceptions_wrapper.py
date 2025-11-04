from functools import wraps
from sqlalchemy.exc import (
    IntegrityError,
    NoResultFound,
    MultipleResultsFound,
    DBAPIError,
    OperationalError,
    DataError,
)
from app.core.exceptions import (
    EntityAlreadyExistsError,
    EntityDoesNotExistError,
    ServiceError,
)

def handle_db_errors(func):
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except IntegrityError:
            raise EntityAlreadyExistsError("Entity already exists")
        except NoResultFound:
            raise EntityDoesNotExistError("Entity not found")
        except (OperationalError, DBAPIError, DataError, MultipleResultsFound) as e:
            raise ServiceError(f"Database error: {str(e)}")
    return wrapper