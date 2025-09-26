"""Shared Jinja2 template loader configuration."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Iterable

from fastapi.templating import Jinja2Templates


from jinja2 import ChoiceLoader, Environment, FileSystemLoader, select_autoescape

from jinja2 import ChoiceLoader, Environment, FileSystemLoader



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

    existing_dirs = [path for path in candidate_dirs if path.exists()]
    if not existing_dirs:
        raise RuntimeError(
            "No template directories were found. Ensure 'backend/templates' "
            "exists in the project checkout."
        )

    # Build a dedicated Jinja2 environment that is aware of every template
    # directory from the outset.  Instantiating ``Jinja2Templates`` with the
    # environment avoids reassigning loaders after initialisation which can be
    # fragile on some platforms and older dependency versions.
    loaders = [FileSystemLoader(str(path)) for path in existing_dirs]
    loader = loaders[0] if len(loaders) == 1 else ChoiceLoader(loaders)

    env = Environment(loader=loader, autoescape=True)
    # ``Jinja2Templates`` requires an initial directory; we point it at the
    # first available folder and then teach the underlying Jinja environment to
    # look in every discovered directory.  ``ChoiceLoader`` keeps FastAPI from
    # caring whether a template lives in ``backend/templates`` or
    # ``backend/app/templates``.
    templates = Jinja2Templates(directory=str(existing_dirs[0]))

    if len(existing_dirs) == 1:
        templates.env.loader = FileSystemLoader(str(existing_dirs[0]))
    else:
        templates.env.loader = ChoiceLoader(
            [FileSystemLoader(str(path)) for path in existing_dirs]
        )


    return Jinja2Templates(env=env)

