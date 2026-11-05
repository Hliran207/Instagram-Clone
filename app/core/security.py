from datetime import UTC, datetime, timedelta

import jwt
from pwdlib import PasswordHash

from app.core.config import settings

PASSWORD_HASHER = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Hash a password using pwdlib with the recommended algorithm = ARGON2."""
    return PASSWORD_HASHER.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a password against a hashed password using pwdlib."""
    return PASSWORD_HASHER.verify(password, hashed_password)


def create_access_token(user_id: int) -> str:
    expire = datetime.now(UTC) + timedelta(minutes=settings.access_token_expire_minutes)
    payload = {
        "sub": str(user_id),
        "exp": expire,
    }
    return jwt.encode(payload, settings.jwt_secret, algorithm="HS256")
