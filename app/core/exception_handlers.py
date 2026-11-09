import logging

from fastapi import Request
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.errors import (
    EmailAlreadyExistsError,
    InstagramError,
    InvalidCredentialsError,
    NotAuthenticatedError,
    UsernameAlreadyExistsError,
    UserNotFoundError,
)

logger = logging.getLogger(__name__)

STATUS_CODES: dict[type[InstagramError], int] = {
    UsernameAlreadyExistsError: 409,
    EmailAlreadyExistsError: 409,
    UserNotFoundError: 404,
    InvalidCredentialsError: 401,
    NotAuthenticatedError: 401,
}


def handle_instagram_error(request: Request, exc: InstagramError) -> JSONResponse:
    status_code = STATUS_CODES.get(type(exc), 400)
    return JSONResponse(
        status_code=status_code,
        content={"error": {"code": exc.code, "message": exc.message}},
    )


def handle_validation_error(
    request: Request, exc: RequestValidationError
) -> JSONResponse:
    fields = [
        {
            "field": ".".join(str(part) for part in err["loc"][1:]),
            "code": err["type"],
            "message": err["msg"],
        }
        for err in exc.errors()
    ]
    return JSONResponse(
        status_code=422,
        content={
            "error": {
                "code": "validation_error",
                "message": "Invalid request",
                "fields": fields,
            }
        },
    )


def handle_unexpected_error(request: Request, exc: Exception) -> JSONResponse:
    logger.error("Unexpected error", exc_info=exc)
    return JSONResponse(
        status_code=500,
        content={
            "error": {"code": "internal_error", "message": "Something went wrong"}
        },
    )
