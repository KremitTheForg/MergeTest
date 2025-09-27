"""Regression tests for the authentication flow."""

from __future__ import annotations

import sys
from pathlib import Path
from types import SimpleNamespace

import pytest
from fastapi.testclient import TestClient

PROJECT_ROOT = Path(__file__).resolve().parents[2]
BACKEND_DIR = PROJECT_ROOT / "backend"

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app import crud  # noqa: E402
from app.main import app  # noqa: E402
from app.database import get_db  # noqa: E402


@pytest.fixture
def test_client():
    """Return a ``TestClient`` with the database dependency disabled."""

    def _override_get_db():
        yield None

    app.dependency_overrides[get_db] = _override_get_db
    try:
        yield TestClient(app)
    finally:
        app.dependency_overrides.pop(get_db, None)


def test_verify_password_returns_false_for_plaintext_hash():
    """Legacy plaintext passwords should not crash password verification."""

    assert crud.verify_password("hunter2", "not-a-hash") is False


def test_login_returns_401_for_legacy_plaintext_password(monkeypatch, test_client):
    """Legacy users with plaintext passwords should receive a 401 response."""

    legacy_user = SimpleNamespace(
        id=1,
        username="legacy",
        email="legacy@example.com",
        hashed_password="not-a-hash",
    )

    monkeypatch.setattr(crud, "get_user_by_email", lambda db, email: legacy_user)

    response = test_client.post(
        "/auth/login",
        data={"email": "legacy@example.com", "password": "hunter2"},
        follow_redirects=False,
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"
