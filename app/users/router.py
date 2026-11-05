from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from app.core.db import get_db
from app.users.models import User
from app.users.schemas import UserCreate, UserResponse
from app.users.service import register_user

router = APIRouter(tags=["users"])
SessionDep = Annotated[Session, Depends(get_db)]


@router.post(
    "/auth/register", status_code=status.HTTP_201_CREATED, response_model=UserResponse
)
def add_user(data: UserCreate, session: SessionDep) -> User:
    return register_user(session, data)
