"""Portal routes for profile management (HTML rendering flows)."""
from __future__ import annotations

from pathlib import Path
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Request, UploadFile, File, Form
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse

from fastapi.templating import Jinja2Templates

from sqlalchemy.orm import Session

from .. import models, schemas, crud, database
from ..services import profile as profile_service
from ..core.templates import get_templates

router = APIRouter(prefix="/portal", tags=["portal"])
BASE_DIR = Path(__file__).resolve().parent.parent.parent
templates = get_templates()
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
FRONTEND_DIST_DIR = BASE_DIR / "static" / "forms"
FRONTEND_INDEX_FILE = FRONTEND_DIST_DIR / "index.html"


def get_current_user(request: Request, db: Session = Depends(database.get_db)) -> models.User:
    user = request.session.get("user")
    if not user:
        raise HTTPException(status_code=401, detail="Not authenticated")

    db_user = db.query(models.User).filter(models.User.id == user["id"]).first()
    if not db_user:
        raise HTTPException(status_code=401, detail="User not found")
    return db_user


@router.get("/profile", response_class=HTMLResponse)
def profile_form(
    request: Request,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user),
):
    candidate = crud.get_candidate_by_user(db, user_id=int(current_user.id))
    if not candidate:
        return templates.TemplateResponse(
            "dashboard.html",
            {
                "request": request,
                "user": current_user,
                "error": "No candidate record associated with this account.",
            },
        )

    if FRONTEND_INDEX_FILE.exists():
        return FileResponse(FRONTEND_INDEX_FILE, media_type="text/html")

    profile = crud.get_or_create_profile(db, candidate.id)
    return templates.TemplateResponse(
        "profile.html",
        {
            "request": request,
            "user": current_user,
            "candidate": candidate,
            "profile": profile,
        },
    )


@router.post("/profile", response_class=HTMLResponse)
def profile_submit(
    request: Request,
    summary: Optional[str] = Form(None),
    skills: Optional[str] = Form(None),
    linkedin: Optional[str] = Form(None),
    address: Optional[str] = Form(None),
    job_title: Optional[str] = Form(None),
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user),
):
    candidate = crud.get_candidate_by_user(db, user_id=int(current_user.id))
    if not candidate:
        raise HTTPException(status_code=400, detail="No candidate linked to this user")

    candidate.job_title = (job_title or "").strip()
    db.add(candidate)
    db.commit()
    db.refresh(candidate)

    update = schemas.CandidateProfileUpdate(
        summary=summary, skills=skills, linkedin=linkedin, address=address
    )
    profile = crud.update_profile(db, candidate.id, update)

    return templates.TemplateResponse(
        "profile.html",
        {
            "request": request,
            "user": current_user,
            "candidate": candidate,
            "profile": profile,
            "saved": True,
        },
    )


@router.post("/profile/upload")
async def upload_file(
    request: Request,
    kind: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(get_current_user),
):
    candidate = crud.get_candidate_by_user(db, user_id=int(current_user.id))
    if not candidate:
        raise HTTPException(status_code=400, detail="No candidate linked to this user")

    await profile_service.save_profile_upload(
        candidate=candidate, kind=kind, file=file, db=db
    )
    await file.close()
    return RedirectResponse(url="/portal/profile", status_code=303)


@router.post("/profile/admin/{user_id}/upload")
async def admin_upload_file(
    user_id: int,
    kind: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(database.get_db),
):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    candidate = crud.get_candidate_by_user(db, user_id=int(db_user.id))
    if not candidate:
        raise HTTPException(status_code=400, detail="No candidate linked to this user")

    await profile_service.save_profile_upload(
        candidate=candidate, kind=kind, file=file, db=db
    )
    await file.close()
    return RedirectResponse(url=f"/portal/profile/admin/{db_user.id}", status_code=303)


@router.get("/profile/admin/{user_id}", response_class=HTMLResponse)
def profile_admin(
    user_id: int,
    request: Request,
    db: Session = Depends(database.get_db),
):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    candidate = crud.get_candidate_by_user(db, user_id=int(db_user.id))
    if not candidate:
        return templates.TemplateResponse(
            "profile.html",
            {
                "request": request,
                "user": db_user,
                "candidate": None,
                "profile": None,
                "admin_view": True,
                "error": "No candidate record linked to this user.",
            },
        )

    if FRONTEND_INDEX_FILE.exists():
        return FileResponse(FRONTEND_INDEX_FILE, media_type="text/html")

    profile = crud.get_or_create_profile(db, candidate.id)
    return templates.TemplateResponse(
        "profile.html",
        {
            "request": request,
            "user": db_user,
            "candidate": candidate,
            "profile": profile,
            "admin_view": True,
        },
    )


@router.post("/profile/admin/{user_id}")
def admin_save_profile(
    user_id: int,
    request: Request,
    summary: Optional[str] = Form(None),
    skills: Optional[str] = Form(None),
    linkedin: Optional[str] = Form(None),
    address: Optional[str] = Form(None),
    job_title: Optional[str] = Form(None),
    db: Session = Depends(database.get_db),
):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")

    candidate = crud.get_candidate_by_user(db, user_id=int(db_user.id))
    if not candidate:
        candidate = models.Candidate(
            user_id=db_user.id,
            email=db_user.email or "",
            first_name="",
            last_name="",
            status="Applied",
        )
        db.add(candidate)
        db.flush()

    candidate.job_title = (job_title or "").strip()
    db.add(candidate)
    db.commit()
    db.refresh(candidate)

    update = schemas.CandidateProfileUpdate(
        summary=summary, skills=skills, linkedin=linkedin, address=address
    )
    crud.update_profile(db, candidate.id, update)

    return RedirectResponse(
        url=f"/portal/profile/admin/{db_user.id}?saved=1", status_code=303
    )
