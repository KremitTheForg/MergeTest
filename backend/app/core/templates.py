"""Shared Jinja2 template loader configuration."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Iterable

from fastapi.templating import Jinja2Templates
from jinja2 import ChoiceLoader, FileSystemLoader


@lru_cache()
def get_templates() -> Jinja2Templates:
    """Return a configured ``Jinja2Templates`` instance."""

    module_root = Path(__file__).resolve().parents[2]
    project_root = module_root.parent
    cwd = Path.cwd()

    def _candidate_paths(root: Path) -> Iterable[Path]:
        yield root / "templates"
        yield root / "app" / "templates"
        yield root / "backend" / "templates"
        yield root / "backend" / "app" / "templates"

    candidate_dirs: list[Path] = []
    seen: set[Path] = set()

    for root in (module_root, project_root, cwd):
        for candidate in _candidate_paths(root):
            if not candidate.exists():
                continue

            resolved = candidate.resolve()
            if resolved not in seen:
                seen.add(resolved)
                candidate_dirs.append(resolved)

    if not candidate_dirs:
        raise RuntimeError(
            "No template directories were found. Ensure the repository checkout "
            "contains the expected 'backend/templates' or 'backend/app/templates' "
            "folders."
        )

    templates = Jinja2Templates(directory=str(candidate_dirs[0]))

    if len(candidate_dirs) == 1:
        templates.env.loader = FileSystemLoader(str(candidate_dirs[0]))
    else:
        templates.env.loader = ChoiceLoader(
            [FileSystemLoader(str(path)) for path in candidate_dirs]
        )

    return templates

