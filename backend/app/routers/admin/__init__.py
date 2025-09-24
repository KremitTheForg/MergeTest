"""Admin-facing HTML views grouped by domain."""

from .router import router  # noqa: F401
from . import applicants  # noqa: F401
from . import dashboard  # noqa: F401
from . import users  # noqa: F401

__all__ = ["router"]
