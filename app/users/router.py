from fastapi import APIRouter, status

from app.core.db import SessionDep
from app.core.security import create_access_token
from app.users.dependencies import CurrentUser
from app.users.models import User
from app.users.repository import get_user_by_id
from app.users.schemas import TokenResponse, UserCreate, UserLogin, UserResponse
from app.users.service import authenticate_user, register_user

router = APIRouter(tags=["users"])


@router.post(
    "/auth/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse
)
def add_user(data: UserCreate, session: SessionDep) -> User:
    return register_user(session, data)


@router.post("/auth/login", response_model=TokenResponse)
def login_user(data: UserLogin, session: SessionDep) -> TokenResponse:
    user = authenticate_user(session, data.login, data.password)
    return TokenResponse(access_token=create_access_token(user.id))


@router.get("/users/me", response_model=UserResponse)
def get_current_user(user: CurrentUser, session: SessionDep) -> User:
    return get_user_by_id(session, user.id)
