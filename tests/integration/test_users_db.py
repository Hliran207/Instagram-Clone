import pytest
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.users.models import User


def make_user(username: str, email: str) -> User:
    return User(username=username, email=email, password_hash="x")


def test_username_is_unique_case_insensitive(db_session: Session) -> None:
    db_session.add(make_user("liran", "liran@x.com"))
    db_session.flush()

    db_session.add(make_user("Liran", "other@x.com"))
    with pytest.raises(IntegrityError) as exc_info:
        db_session.flush()

    assert "uq_users_username_lower" in str(exc_info.value)


def test_data_does_not_leak_between_tests(db_session: Session) -> None:
    db_session.add(make_user("liran", "liran@x.com"))
    db_session.commit()

    assert db_session.query(User).count() == 1
