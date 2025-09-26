"""Shared Jinja2 template loader configuration."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Iterable

from fastapi.templating import Jinja2Templates

from jinja2 import ChoiceLoader, Environment, FileSystemLoader, select_autoescape


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

    module_root = Path(__file__).resolve().parents[2]
    project_root = module_root.parent
    cwd = Path.cwd()

    def _candidate_paths(root: Path) -> Iterable[Path]:
        yield root / "templates"
        yield root / "app" / "templates"
        yield root / "backend" / "templates"
        yield root / "backend" / "app" / "templates"

    discovered_dirs: list[Path] = []
    seen: set[Path] = set()

    for root in (module_root, project_root, cwd):
        for candidate in _candidate_paths(root):
            if not candidate.exists():
                continue

            resolved = candidate.resolve()
            if resolved not in seen:
                seen.add(resolved)
                discovered_dirs.append(resolved)

    if not discovered_dirs:
        raise RuntimeError(
            "No template directories were found. Ensure the repository checkout "
            "contains the expected 'backend/templates' or 'backend/app/templates' "
            "folders."
        )

    loaders = [FileSystemLoader(str(path)) for path in discovered_dirs]
    loader = loaders[0] if len(loaders) == 1 else ChoiceLoader(loaders)

    env = Environment(
        loader=loader,
        autoescape=select_autoescape(("html", "htm", "xml")),
    )

    return Jinja2Templates(env=env)

