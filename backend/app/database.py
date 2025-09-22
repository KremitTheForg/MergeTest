import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load variables from .env file
load_dotenv()

# Reads DATABASE_URL from .env
DATABASE_URL = os.getenv("DATABASE_URL")
# Engine (connection pool to PostgreSQL)
engine = create_engine(DATABASE_URL)
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