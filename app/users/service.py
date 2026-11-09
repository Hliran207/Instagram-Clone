from sqlalchemy.orm import Session

from app.core.errors import InvalidCredentialsError, UserNotFoundError
from app.core.security import hash_password, verify_password
from app.users.models import User
from app.users.repository import create_user, get_user_by_email, get_user_by_username
from app.users.schemas import UserCreate, UserPublic, UserUpdate


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


# This is a dummy hash to use when the user is not found.
# It used to prevent user enumeration attacks - timing attacks - the attacker will not
# know if the username or email is correct.

DUMMY_HASH = hash_password("not-a-real-password")


def authenticate_user(session: Session, login: str, password: str) -> User:
    if "@" in login:
        user = get_user_by_email(session, login)
    else:
        user = get_user_by_username(session, login)
    if not user:
        verify_password(password, DUMMY_HASH)
        raise InvalidCredentialsError("Invalid credentials")
    if not verify_password(password, user.password_hash):
        raise InvalidCredentialsError("Invalid credentials")
    return user


def update_user(session: Session, user: User, data: UserUpdate) -> User:
    changes = data.model_dump(exclude_unset=True)
    for key, value in changes.items():
        setattr(user, key, value)
    session.commit()
    return user


def get_user_profile(session: Session, username) -> UserPublic | None:
    user_response = get_user_by_username(session, username)
    if user_response is None:
        raise UserNotFoundError("User not found")
    return user_response
