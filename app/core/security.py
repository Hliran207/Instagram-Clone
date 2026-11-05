from pwdlib import PasswordHash

PASSWORD_HASHER = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """Hash a password using pwdlib with the recommended algorithm = ARGON2."""
    return PASSWORD_HASHER.hash(password)


def verify_password(password: str, hashed_password: str) -> bool:
    """Verify a password against a hashed password using pwdlib."""
    return PASSWORD_HASHER.verify(password, hashed_password)
