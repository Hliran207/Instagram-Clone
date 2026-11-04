from fastapi import FastAPI

from app.core.errors import InstagramError, UserNotFoundError
from app.core.exception_handlers import handle_instagram_error

app = FastAPI(title="Instagram API", description="API for the Instagram project")

app.add_exception_handler(InstagramError, handle_instagram_error)


@app.get("/health")
def health_check() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/users")
def get_user(user_id: int) -> dict[str, str]:
    raise UserNotFoundError(f"User {user_id} not found")
