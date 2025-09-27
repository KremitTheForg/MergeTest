"""Regression tests for authentication edge cases."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

PROJECT_ROOT = Path(__file__).resolve().parents[2]
BACKEND_DIR = PROJECT_ROOT / "backend"

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app import crud, models  # noqa: E402  (import after path tweak)
from app.database import Base, get_db  # noqa: E402  (import after path tweak)
from app.main import app  # noqa: E402  (import after path tweak)


@pytest.fixture(name="client_with_db")
def _client_with_db():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    Base.metadata.create_all(bind=engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db

    client = TestClient(app)

    try:
        yield client, TestingSessionLocal
    finally:
        app.dependency_overrides.pop(get_db, None)
        Base.metadata.drop_all(bind=engine)
        engine.dispose()


def test_verify_password_returns_false_for_plaintext_hash():
    """Unparseable hashes should be treated as invalid credentials."""

    assert crud.verify_password("pw", "plain") is False


def test_login_returns_401_for_plaintext_hash(client_with_db):
    """Users with broken hashes should see a 401 response when logging in."""

    client, TestingSessionLocal = client_with_db

    with TestingSessionLocal() as db:
        user = models.User(username="plain", email="plain@example.com", hashed_password="plain")
        db.add(user)
        db.commit()

    response = client.post("/auth/login", data={"email": "plain@example.com", "password": "pw"})

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"
