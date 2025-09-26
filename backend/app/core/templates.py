"""Shared Jinja2 template loader configuration."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path

from fastapi.templating import Jinja2Templates
from jinja2 import ChoiceLoader, FileSystemLoader


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

    candidate_dirs = [
        base_dir / "templates",
        base_dir / "app" / "templates",
    ]

    existing_dirs = [str(path) for path in candidate_dirs if path.exists()]
    if not existing_dirs:
        raise RuntimeError(
            "No template directories were found. Ensure 'backend/templates' "
            "exists in the project checkout."
        )

    # ``Jinja2Templates`` requires an initial directory; afterward we swap in a
    # ``ChoiceLoader`` so lookups span every available template folder.
    templates = Jinja2Templates(directory=existing_dirs[0])

    if len(existing_dirs) > 1:
        templates.env.loader = ChoiceLoader(
            [FileSystemLoader(path) for path in existing_dirs]
        )

    return templates

