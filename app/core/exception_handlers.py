from fastapi import Request
from fastapi.responses import JSONResponse

from app.core.errors import InstagramError, UserAlreadyExistsError, UserNotFoundError

STATUS_CODES: dict[type[InstagramError], int] = {
    UserAlreadyExistsError: 409,
    UserNotFoundError: 404,
}


def handle_instagram_error(request: Request, exc: InstagramError) -> JSONResponse:
    status_code = STATUS_CODES.get(type(exc), 400)
    return JSONResponse(
        status_code=status_code,
        content={"error": {"code": exc.code, "message": exc.message}},
    )
