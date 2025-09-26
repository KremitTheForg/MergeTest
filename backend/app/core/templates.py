"""Shared Jinja2 template loader configuration."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from fastapi.templating import Jinja2Templates


@lru_cache()
def get_templates() -> Jinja2Templates:
    """Return a configured ``Jinja2Templates`` instance.

    The legacy UI lives under ``backend/templates`` while a handful of
    feature-specific snippets still reside in ``backend/app/templates``.
    When developers run the project from different working directories,
    FastAPI must be able to locate templates from both locations.  Using a
    cached helper keeps the configuration in a single place and avoids
    subtle path mistakes across individual routers.
    """

    # ``backend/app/core/templates.py`` -> ``backend/app`` -> ``backend``
    base_dir = Path(__file__).resolve().parents[2]

    primary_dir = base_dir / "templates"
    app_templates_dir = base_dir / "app" / "templates"

    templates = Jinja2Templates(directory=str(primary_dir))

    # Ensure secondary template locations remain discoverable.  ``exists``
    # guards against missing optional folders (e.g. during partial checkouts).
    for extra_dir in (app_templates_dir,):
        if extra_dir.exists():
            extra_path = str(extra_dir)
            if extra_path not in templates.env.loader.searchpath:
                templates.env.loader.searchpath.append(extra_path)

    return templates

