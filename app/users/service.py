from sqlalchemy.orm import Session

from app.core.errors import InvalidCredentialsError
from app.core.security import hash_password, verify_password
from app.users.models import User
from app.users.repository import create_user, get_user_by_email, get_user_by_username
from app.users.schemas import UserCreate


def register_user(session: Session, data: UserCreate) -> User:
    password_hash = hash_password(data.password)
    user = create_user(
        session,
        username=data.username,
        email=data.email,
        password_hash=password_hash,
        full_name=data.full_name,
        bio=data.bio,
    )
    session.commit()
    return user


DUMMY_HASH = hash_password("not-a-real-password")


def authenticate_user(session: Session, login: str, password: str) -> User:
    if "@" in login:
        user = get_user_by_email(session, login)
    else:
        user = get_user_by_username(session, login)
    if not user:
        verify_password(DUMMY_PASSWORD, user.password_hash)
        raise InvalidCredentialsError("Invalid credentials")
    if not verify_password(password, user.password_hash):
        raise InvalidCredentialsError("Invalid credentials")
    return user
