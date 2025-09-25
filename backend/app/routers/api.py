"""JSON API surface that mirrors the existing HTML flows."""
from __future__ import annotations

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, File, Form
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.database import get_db
from app.services import admin as admin_service
from app.services import profile as profile_service

router = APIRouter(prefix="/api/v1", tags=["api"])


def get_session_user(
    request: Request, db: Session = Depends(get_db)
) -> models.User:
    session_data = request.session.get("user")
    if not session_data:
        raise HTTPException(status_code=401, detail="Not authenticated")

    db_user = db.query(models.User).filter(models.User.id == session_data["id"]).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="User not found")
    return db_user


@router.get("/me", response_model=schemas.MeResponse)
def get_me(
    current_user: models.User = Depends(get_session_user),
    db: Session = Depends(get_db),
):
    candidate = crud.get_candidate_by_user(db, user_id=int(current_user.id))
    profile = None
    if candidate:
        profile = crud.get_profile(db, candidate.id)

    return {
        "user": schemas.UserOut.model_validate(current_user),
        "candidate": schemas.CandidateOut.model_validate(candidate)
        if candidate
        else None,
        "profile": schemas.CandidateProfileOut.model_validate(profile)
        if profile
        else None,
    }


@router.get("/admin/metrics", response_model=schemas.AdminMetrics)
def admin_metrics(
    current_user: models.User = Depends(get_session_user),
    db: Session = Depends(get_db),
):
    return admin_service.get_dashboard_metrics(db)


@router.get("/admin/candidates", response_model=schemas.CandidateListResponse)
def admin_candidates(
    current_user: models.User = Depends(get_session_user),
    db: Session = Depends(get_db),
):
    rows = admin_service.fetch_candidates_with_profiles(db)
    results = []
    for candidate, profile in rows:
        results.append(
            schemas.CandidateWithProfile(
                candidate=schemas.CandidateOut.model_validate(candidate),
                profile=schemas.CandidateProfileOut.model_validate(profile)
                if profile
                else None,
            )
        )
    return {"results": results}


@router.get("/admin/workers", response_model=schemas.WorkerListResponse)
def admin_workers(
    role: Optional[str] = None,
    status: Optional[str] = None,
    date_from: Optional[str] = None,
    date_to: Optional[str] = None,
    q: Optional[str] = None,
    current_user: models.User = Depends(get_session_user),
    db: Session = Depends(get_db),
):
    result = admin_service.query_worker_users(
        db,
        role=role,
        status=status,
        date_from=date_from,
        date_to=date_to,
        q=q,
    )

    filters = schemas.WorkerQueryFilters(
        role=result.filters.role,
        status=result.filters.status,
        date_from=result.filters.date_from,
        date_to=result.filters.date_to,
        q=result.filters.q,
    )

    # Preserve the ordering from the dataclass result
    ordered_results = [
        schemas.WorkerUserOut(
            user=schemas.UserOut.model_validate(user),
            candidate=schemas.CandidateOut.model_validate(result.user_candidates[user.id]),
        )
        for user in result.users
    ]

    return {
        "results": ordered_results,
        "filters": filters,
        "roles": result.roles,
        "status_options": result.status_options,
    }


@router.get("/admin/applicants", response_model=schemas.ApplicantListResponse)
def admin_applicants(
    current_user: models.User = Depends(get_session_user),
    db: Session = Depends(get_db),
):
    applicants = admin_service.list_applicants(db)
    return {
        "results": [
            schemas.CandidateOut.model_validate(candidate)
            for candidate in applicants
        ]
    }


@router.put("/portal/profile", response_model=schemas.ProfileResponse)
def update_profile(
    payload: schemas.ProfileUpdatePayload,
    current_user: models.User = Depends(get_session_user),
    db: Session = Depends(get_db),
):
    candidate = crud.get_candidate_by_user(db, user_id=int(current_user.id))
    if not candidate:
        raise HTTPException(status_code=400, detail="No candidate linked to this user")

    candidate.job_title = (payload.job_title or "").strip()
    db.add(candidate)
    db.commit()
    db.refresh(candidate)

    profile_data = payload.dict(exclude={"job_title"}, exclude_unset=True)
    update = schemas.CandidateProfileUpdate(**profile_data)
    profile = crud.update_profile(db, candidate.id, update)

    return {
        "candidate": schemas.CandidateOut.model_validate(candidate),
        "profile": schemas.CandidateProfileOut.model_validate(profile),
    }


@router.post("/portal/profile/upload", response_model=schemas.ProfileUploadResponse)
async def upload_profile_asset(
    kind: str = Form(...),
    file: UploadFile = File(...),
    current_user: models.User = Depends(get_session_user),
    db: Session = Depends(get_db),
):
    candidate = crud.get_candidate_by_user(db, user_id=int(current_user.id))
    if not candidate:
        raise HTTPException(status_code=400, detail="No candidate linked to this user")

    normalized_kind = "photo" if kind == "picture" else kind
    path = await profile_service.save_profile_upload(
        candidate=candidate, kind=kind, file=file, db=db
    )
    await file.close()

    return {
        "candidate_id": candidate.id,
        "kind": normalized_kind,
        "path": path,
    }
