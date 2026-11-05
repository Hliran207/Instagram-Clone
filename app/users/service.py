from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.users.models import User
from app.users.repository import create_user
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
