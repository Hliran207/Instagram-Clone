import os

# Tests always run against a separate database, never the dev one.
# Must run before importing app code, because settings are read at import time.
os.environ["POSTGRES_DB"] = "instagram_test"
from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import Connection
from sqlalchemy.orm import Session

from app.core.db import engine, get_db
from app.main import app


@pytest.fixture
def connection() -> Iterator[Connection]:
    connection = engine.connect()
    transaction = connection.begin()

    yield connection

    transaction.rollback()
    connection.close()


@pytest.fixture
def db_session(connection: Connection) -> Iterator[Session]:
    session = Session(bind=connection, join_transaction_mode="create_savepoint")
    yield session
    session.close()


@pytest.fixture
def client(connection: Connection) -> Iterator[TestClient]:
    def get_test_db() -> Iterator[Session]:
        session = Session(bind=connection, join_transaction_mode="create_savepoint")
        try:
            yield session
        finally:
            session.close()

    app.dependency_overrides[get_db] = get_test_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
