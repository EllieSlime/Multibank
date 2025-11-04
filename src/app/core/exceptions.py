from fastapi import HTTPException, status

class ApiError(Exception):
    """base exception class"""

    def __init__(self, detail: str = "Service is unavailable",status_code: int = 500, name: str = "Api"):
        self.detail = detail
        self.status_code = status_code
        self.name = name
        super().__init__(self.detail, self.name)


class ServiceError(ApiError):
    def __init__(self, detail="Service is unavailable"):
        super().__init__(detail=detail, status_code=503)

class EntityDoesNotExistError(ApiError):
    def __init__(self, detail="Entity does not exist"):
        super().__init__(detail=detail, status_code=404)

class EntityAlreadyExistsError(ApiError):
    def __init__(self, detail="Entity already exists"):
        super().__init__(detail=detail, status_code=409)

class AuthenticationFailedError(ApiError):
    def __init__(self, detail="Authentication failed"):
        super().__init__(detail=detail, status_code=401)

class InvalidTokenError(ApiError):
    def __init__(self, detail="Invalid token"):
        super().__init__(detail=detail, status_code=403)

class ValidationFailed(ApiError):
    def __init__(self, detail="Validation failed"):
        super().__init__(detail=detail, status_code=422)

