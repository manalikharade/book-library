"""Database engine and session management with pool settings and error handling."""
import logging
import os

from sqlalchemy import create_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import declarative_base, sessionmaker

from app.config import get_settings

logger = logging.getLogger(__name__)

# Use TEST_DATABASE_URL when set (e.g. by pytest) so tests can run without PostgreSQL
if os.environ.get("TEST_DATABASE_URL"):
    DATABASE_URL = os.environ["TEST_DATABASE_URL"]
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {},
        echo=False,
    )
else:
    _settings = get_settings()
    DATABASE_URL = (
        f"postgresql+psycopg://{_settings.db_user}:{_settings.db_password}"
        f"@{_settings.db_host}:{_settings.db_port}/{_settings.db_name}"
    )
    engine = create_engine(
        DATABASE_URL,
        pool_size=_settings.db_pool_size,
        max_overflow=_settings.db_max_overflow,
        pool_recycle=_settings.db_pool_recycle,
        echo=False,
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Dependency that yields a DB session and handles rollback on error."""
    db = SessionLocal()
    try:
        yield db
    except SQLAlchemyError as e:
        logger.exception("Database session error: %s", e)
        db.rollback()
        raise
    finally:
        db.close()


def init_db() -> None:
    """Create all tables. Call on startup."""
    Base.metadata.create_all(bind=engine)
    logger.info("Database tables initialized")
