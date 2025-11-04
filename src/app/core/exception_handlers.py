from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from app.core.exceptions import ServiceError, EntityAlreadyExistsError, EntityDoesNotExistError, InvalidTokenError, AuthenticationFailedError, ValidationFailed


def add_exception_handlers(app: FastAPI):
    @app.exception_handler(EntityDoesNotExistError)
    async def does_not_exist_handler(request: Request, exc: EntityDoesNotExistError):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )
    
    @app.exception_handler(ValidationFailed)
    async def validation_failed_handler(request: Request, exc: ValidationFailed):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail},
        )
    
    @app.exception_handler(ServiceError)
    async def service_is_not_working_error(request: Request, exc: ServiceError):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )
    
    @app.exception_handler(EntityAlreadyExistsError)
    async def already_exists_handler(request: Request, exc: EntityAlreadyExistsError):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )
    
    @app.exception_handler(InvalidTokenError)
    async def invalid_token_handler(request: Request, exc: InvalidTokenError):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )
    
    @app.exception_handler(AuthenticationFailedError)
    async def authentication_failed_handler(request: Request, exc: AuthenticationFailedError):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.detail}
        )