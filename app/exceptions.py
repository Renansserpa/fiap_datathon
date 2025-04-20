# %%
from typing import Any

from fastapi import HTTPException, status


class DetailedHTTPException(HTTPException):
    STATUS_CODE = status.HTTP_500_INTERNAL_SERVER_ERROR
    DETAIL = "Server error"

    def __init__(self, **kwargs: dict[str, Any]) -> None:
        super().__init__(status_code=self.STATUS_CODE, detail=self.DETAIL, **kwargs)


class PermissionDenied(DetailedHTTPException):
    STATUS_CODE = status.HTTP_403_FORBIDDEN
    DETAIL = "Permissão negada. Esta operação só pode ser realizada pelo próprio usuário ou o admin."


class UserAlreadyExists(DetailedHTTPException):
    STATUS_CODE = status.HTTP_409_CONFLICT
    DETAIL = "Email de usuário já existente na base de dados."


class UserNotFound(DetailedHTTPException):
    STATUS_CODE = status.HTTP_404_NOT_FOUND
    DETAIL = "Usuário não encontrado. Email ou senha estão incorretos"


class ExpiredToken(DetailedHTTPException):
    STATUS_CODE = status.HTTP_410_GONE
    DETAIL = "Authentication token expired"


class NotAuthenticated(DetailedHTTPException):
    STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    DETAIL = "User not authenticated. Could not validate credentials"

    def __init__(self) -> None:
        super().__init__(headers={"WWW-Authenticate": "Bearer"})