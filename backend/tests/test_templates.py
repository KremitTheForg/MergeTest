"""Integration tests for the shared Jinja2 template loader."""

from __future__ import annotations

import sys
from pathlib import Path

from jinja2.loaders import ChoiceLoader, FileSystemLoader
from starlette.requests import Request

PROJECT_ROOT = Path(__file__).resolve().parents[2]
BACKEND_DIR = PROJECT_ROOT / "backend"

if str(BACKEND_DIR) not in sys.path:
    sys.path.insert(0, str(BACKEND_DIR))

from app.core.templates import get_templates  # noqa: E402  (import after path tweak)


def _collect_search_paths(loader: FileSystemLoader | ChoiceLoader) -> set[Path]:
    """Return the set of directories searched by ``loader``."""

    if isinstance(loader, FileSystemLoader):
        return {Path(path).resolve() for path in loader.searchpath}

    search_paths: set[Path] = set()
    for subloader in loader.loaders:  # type: ignore[attr-defined]
        if isinstance(subloader, FileSystemLoader):
            search_paths.update(Path(path).resolve() for path in subloader.searchpath)

    return search_paths


def test_login_template_is_available():
    """The shared loader should expose the login template regardless of cwd."""

    get_templates.cache_clear()
    templates = get_templates()

    template = templates.get_template("login.html")
    assert Path(template.filename).name == "login.html"


def test_expected_template_directories_are_registered():
    """Both legacy and app template directories must be registered."""

    expected_dirs = {
        path.resolve()
        for path in (BACKEND_DIR / "templates", BACKEND_DIR / "app" / "templates")
        if path.exists()
    }

    get_templates.cache_clear()
    templates = get_templates()

    search_paths = _collect_search_paths(templates.env.loader)  # type: ignore[arg-type]

    assert expected_dirs.issubset(search_paths)


def test_login_template_renders_successfully():
    """Rendering the login template via ``TemplateResponse`` should succeed."""

    get_templates.cache_clear()
    templates = get_templates()

    scope = {
        "type": "http",
        "method": "GET",
        "path": "/auth/login",
        "headers": [],
        "query_string": b"",
        "client": ("test", 123),
        "server": ("testserver", 80),
        "scheme": "http",
    }

    request = Request(scope)
    response = templates.TemplateResponse("login.html", {"request": request})

    assert response.status_code == 200
    assert "<form" in response.body.decode()
