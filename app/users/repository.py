from sqlalchemy import func, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.core.errors import EmailAlreadyExistsError, UsernameAlreadyExistsError
from app.users.models import User


def create_user(
    session: Session,
    username: str,
    email: str,
    password_hash: str,
    full_name: str | None,
    bio: str | None,
) -> User:
    user = User(
        username=username,
        email=email,
        password_hash=password_hash,
        full_name=full_name,
        bio=bio,
    )
    session.add(user)
    try:
        session.flush()
    except IntegrityError as err:
        if err.orig.diag.constraint_name == "uq_users_username_lower":
            raise UsernameAlreadyExistsError("Username already taken") from err
        if err.orig.diag.constraint_name == "uq_users_email_lower":
            raise EmailAlreadyExistsError("Email already taken") from err
        raise
    return user


def get_user_by_username(session: Session, username: str) -> User | None:
    query = select(User).where(func.lower(User.username) == username.lower())
    return session.scalar(query)


def get_user_by_email(session: Session, email: str) -> User | None:
    query = select(User).where(func.lower(User.email) == email.lower())
    return session.scalar(query)
