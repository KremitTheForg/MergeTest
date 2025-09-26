"""ORM models used by the FastAPI backend."""

from __future__ import annotations


from importlib import import_module
from typing import Iterable


from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, DateTime, ForeignKey, Identity
from sqlalchemy.sql import func

from app.database import Base


__all__ = ["Candidate", "User", "CandidateProfile"]



class Candidate(Base):
    __tablename__ = "candidates"

    id: Mapped[int] = mapped_column(Integer, Identity(always=False), primary_key=True, index=True)
    first_name: Mapped[str]
    last_name: Mapped[str]
    email: Mapped[str] = mapped_column(unique=True, index=True)
    mobile: Mapped[str | None]
    job_title: Mapped[str | None]
    address: Mapped[str | None]

    status: Mapped[str] = mapped_column(default="Applied")
    applied_on: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now())

    user_id: Mapped[int | None] = mapped_column(
        ForeignKey("users.id"), nullable=True
    )
    user: Mapped["User"] = relationship(back_populates="candidates")
    profile: Mapped["CandidateProfile"] = relationship(back_populates="candidate", uselist=False, cascade="all, delete-orphan")


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, Identity(always=False), primary_key=True, index=True)
    username: Mapped[str] = mapped_column(unique=True, index=True)
    email: Mapped[str] = mapped_column(unique=True, index=True)
    hashed_password: Mapped[str]

    candidates: Mapped[list["Candidate"]] = relationship(back_populates="user", cascade="all, delete-orphan")


class CandidateProfile(Base):
    __tablename__ = "candidate_profiles"

    id: Mapped[int] = mapped_column(Integer, Identity(always=False), primary_key=True, index=True)
    candidate_id: Mapped[int] = mapped_column(ForeignKey("candidates.id"), unique=True)

    summary: Mapped[str | None]
    skills: Mapped[str | None]
    linkedin: Mapped[str | None]
    address: Mapped[str | None]
    resume_path: Mapped[str | None]
    photo_path: Mapped[str | None]

    updated_at: Mapped[DateTime] = mapped_column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now())

    candidate: Mapped["Candidate"] = relationship(back_populates="profile")



def _reexport_models(module: str, names: Iterable[str]) -> None:
    """Import ``module`` and expose the requested ORM classes.

    Some upstream datasets expect additional models (for example
    ``CarePlanGoal``) that may not exist in the project yet.  Rather than
    failing the entire models import when an optional class is missing we
    simply skip re-exporting it.  The module itself is still imported so the
    defined SQLAlchemy models register with ``Base.metadata``.
    """

    imported = import_module(f"{__name__}.{module}")
    exported: list[str] = []

    for name in names:
        try:
            globals()[name] = getattr(imported, name)
        except AttributeError:
            continue
        else:
            exported.append(name)

    if exported:
        __all__.extend(exported)


# Import the richer NDIS domain models so Alembic/Base can discover them while
# gracefully handling optional models that are not part of this codebase yet.
_reexport_models("participant", ("Participant",))
_reexport_models("referral", ("Referral",))
_reexport_models(
    "care_plan",
    (
        "CarePlan",
        "ProspectiveWorkflow",
        "RiskAssessment",
        "CarePlanGoal",
    ),
)
_reexport_models(
    "document",
    (
        "Document",
        "DocumentAccess",
        "DocumentCategory",
        "DocumentNotification",
    ),
)
_reexport_models(
    "document_generation",
    (
        "DocumentGenerationTemplate",
        "GeneratedDocument",
        "DocumentGenerationVariable",
        "DocumentSignature",
    ),
)

# Import the richer NDIS domain models so Alembic/Base can discover them.
# These imports are intentionally placed at the bottom to avoid circular
# references when the modules import ``Candidate`` or ``User`` from here.
from .participant import Participant  # noqa: E402,F401
from .referral import Referral  # noqa: E402,F401
from .care_plan import (
    CarePlan,
    ProspectiveWorkflow,
    RiskAssessment,
    CarePlanGoal,
    CarePlanService,
    RiskAssessment,
    SupportWorker,
    CareTeamMember,
    ParticipantNote,
)  # noqa: E402,F401
from .document import (
    Document,
    DocumentAccess,
    DocumentCategory,
    DocumentNotification,
)  # noqa: E402,F401
from .document_generation import (
    DocumentGenerationTemplate,
    GeneratedDocument,
    DocumentGenerationVariable,
    DocumentSignature,
)  # noqa: E402,F401

