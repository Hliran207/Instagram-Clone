from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError

from app.core.errors import InstagramError
from app.core.exception_handlers import (
    handle_instagram_error,
    handle_unexpected_error,
    handle_validation_error,
)

app = FastAPI(title="Instagram API", description="API for the Instagram project")

app.add_exception_handler(InstagramError, handle_instagram_error)
app.add_exception_handler(RequestValidationError, handle_validation_error)
app.add_exception_handler(Exception, handle_unexpected_error)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}
