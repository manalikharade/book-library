"""Pytest fixtures for API and DB."""
import os
from typing import Generator

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session, sessionmaker

# Use SQLite for tests so pytest runs without PostgreSQL (avoids hang on connection)
os.environ["TEST_DATABASE_URL"] = os.getenv("TEST_DATABASE_URL", "sqlite:///./test.db")

from app.database import Base, get_db
from app.main import app


@pytest.fixture(scope="session")
def db_engine():
    """Session-scoped engine; SQLite when TEST_DATABASE_URL is set in conftest."""
    from app.database import engine
    Base.metadata.create_all(bind=engine)
    return engine


@pytest.fixture(scope="function")
def db_session(db_engine) -> Generator[Session, None, None]:
    """Per-test session that rolls back after the test."""
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=db_engine)
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.rollback()
        session.close()


@pytest.fixture
def client(db_session: Session) -> Generator[TestClient, None, None]:
    """Test client with get_db overridden to use test session."""

    def override_get_db():
        try:
            yield db_session
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()
