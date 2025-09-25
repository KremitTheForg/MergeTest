import os
from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv


# Load variables from .env file
load_dotenv()


def _determine_database_url() -> str:
    """Return a usable database URL for the app.

    The previous implementation assumed ``DATABASE_URL`` was always set and let
    ``create_engine`` raise a cryptic ``ArgumentError`` when it was missing.
    That caused the development server to crash with ``Expected string or URL
    object, got None`` for anyone who had not created a local ``.env`` file.

    We still honour ``DATABASE_URL`` when present, but fall back to a local
    SQLite database under ``backend/app/local.db`` so the app boots out of the
    box.  SQLite requires ``check_same_thread=False`` when accessed from the
    FastAPI threadpool, so the caller can inspect the returned URL to configure
    the engine accordingly.
    """

    env_url = os.getenv("DATABASE_URL")
    if env_url:
        return env_url

    base_dir = Path(__file__).resolve().parent
    sqlite_path = base_dir / "local.db"
    return f"sqlite:///{sqlite_path}"


DATABASE_URL = _determine_database_url()

connect_args = {"check_same_thread": False} if DATABASE_URL.startswith("sqlite") else {}

# Engine (connection pool to PostgreSQL/SQLite)
engine = create_engine(DATABASE_URL, connect_args=connect_args)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base for ORM models
Base = declarative_base()


# Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()