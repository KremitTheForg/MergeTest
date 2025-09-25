# =========================
# Imports
# =========================
from pathlib import Path
import secrets, hashlib

from fastapi import FastAPI, Request, Depends, Form
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, RedirectResponse, FileResponse
from fastapi.templating import Jinja2Templates
from fastapi import HTTPException
from starlette.middleware.sessions import SessionMiddleware
from sqlalchemy.orm import Session
from pydantic import EmailStr

from datetime import datetime, timedelta, timezone
from datetime import datetime, timedelta
from sqlalchemy import or_, func

from app import models
from app.database import Base, engine, get_db
from app.routers import candidates as candidates_router
from app.routers import portal as portal_router
from app.routers import auth as auth_router


# =========================
# App Setup & Configuration
# =========================
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Candidate Intake API")

# Static & uploads (absolute paths)
BASE_DIR = Path(__file__).resolve().parent.parent
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))
app.add_middleware(SessionMiddleware, secret_key="super-secret-key")

FRONTEND_DIST_DIR = BASE_DIR / "static" / "forms"
FRONTEND_INDEX_FILE = FRONTEND_DIST_DIR / "index.html"

app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")
app.mount("/uploads", StaticFiles(directory=str(BASE_DIR / "uploads")), name="uploads")

# Status buckets used by Applicants/Workers views
WORKER_STATUSES = {"Hired", "Employee", "Active"}
APPLICANT_STATUSES_EXCLUDE = WORKER_STATUSES


def _parse_iso_to_utc(raw: str):
    """Parse an ISO8601 string into a timezone-aware UTC datetime."""

    if not raw:
        return None

    try:
        value = datetime.fromisoformat(raw)
    except Exception:
        return None

    if value.tzinfo is None:
        return value.replace(tzinfo=timezone.utc)

    return value.astimezone(timezone.utc)


# =========================
# Public / Authenticated Landing
# =========================
@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    user_session = request.session.get("user")
    if not user_session:
        return RedirectResponse(url="/auth/login", status_code=303)

    db_user = db.query(models.User).filter(models.User.id == user_session["id"]).first()
    candidate = db.query(models.Candidate).filter(models.Candidate.user_id == db_user.id).first()

    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "user": db_user, "candidate": candidate},
    )


@app.get("/candidate-form", response_class=HTMLResponse)
def candidate_form(request: Request):
    if FRONTEND_INDEX_FILE.exists():
        return FileResponse(FRONTEND_INDEX_FILE, media_type="text/html")
    return templates.TemplateResponse("index.html", {"request": request})


# =========================
# Admin: Dashboard
# =========================
@app.get("/admin", response_class=HTMLResponse)
def admin_dashboard(request: Request, db: Session = Depends(get_db)):
    candidates_count = db.query(models.Candidate).count()
    users_count = db.query(models.User).count()
    training_count = 0

    return templates.TemplateResponse(
        "admin_dashboard.html",
        {
            "request": request,
            "candidates_count": candidates_count,
            "users_count": users_count,
            "training_count": training_count,
        },
    )


# =========================
# Admin: Candidates (raw list)
# =========================
@app.get("/admin/candidates", response_class=HTMLResponse)
def list_candidates(request: Request, db: Session = Depends(get_db)):
    rows = (
        db.query(models.Candidate, models.CandidateProfile.resume_path)
        .outerjoin(
            models.CandidateProfile,
            models.CandidateProfile.candidate_id == models.Candidate.id,
        )
        .all()
    )

    candidates = [cand for cand, _ in rows]
    resume_paths = {cand.id: resume_path for cand, resume_path in rows}

    return templates.TemplateResponse(
        "candidates.html",
        {
            "request": request,
            "candidates": candidates,
            "resume_paths": resume_paths,
        },
    )
  
    candidates = db.query(models.Candidate).all()
    return templates.TemplateResponse("candidates.html", {"request": request, "candidates": candidates})


# =========================
# Admin: Workers (Users with worker-status Candidate) + Filters
# =========================
@app.get("/admin/users", response_class=HTMLResponse)
def list_users(request: Request, db: Session = Depends(get_db)):
    # ---- read query params
    role      = (request.query_params.get("role")      or "").strip()
    status    = (request.query_params.get("status")    or "").strip()
    date_from = (request.query_params.get("date_from") or "").strip()
    date_to   = (request.query_params.get("date_to")   or "").strip()
    q         = (request.query_params.get("q")         or "").strip()

    # ---- base candidate filters
    cand_filters = [models.Candidate.status.in_(WORKER_STATUSES)]
    if status:
        cand_filters = [models.Candidate.status == status]
    if role:
        cand_filters.append(models.Candidate.job_title == role)

    # joining date range — using applied_on

    start_dt = _parse_iso_to_utc(date_from)
    end_dt   = _parse_iso_to_utc(date_to)

    def _parse_iso(d: str):
        try:
            value = datetime.fromisoformat(d)
        except Exception:
            return None

        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)

        return value.astimezone(timezone.utc)

            return datetime.fromisoformat(d)
        except Exception:
            return None

    start_dt = _parse_iso(date_from)
    end_dt   = _parse_iso(date_to)

    if start_dt:
        cand_filters.append(models.Candidate.applied_on >= start_dt)
    if end_dt:
        cand_filters.append(models.Candidate.applied_on < (end_dt + timedelta(days=1)))

    # keywords across candidate + user fields
    if q:
        like = f"%{q}%"
        cand_filters.append(
            or_(
                models.Candidate.first_name.ilike(like),
                models.Candidate.last_name.ilike(like),
                models.Candidate.email.ilike(like),
                models.Candidate.mobile.ilike(like),
                models.User.username.ilike(like),
                models.User.email.ilike(like),
            )
        )

    # ---- single-pass query with join
    rows = (
        db.query(models.User, models.Candidate)
          .join(models.Candidate, models.Candidate.user_id == models.User.id)
          .filter(*cand_filters)
          .order_by(func.lower(models.User.username))
          .all()
    )

    users = [u for (u, _c) in rows]
    user_candidates = {u.id: c for (u, c) in rows}

    # ---- dropdown data
    roles = [
        r for (r,) in (
            db.query(models.Candidate.job_title)
              .filter(models.Candidate.status.in_(WORKER_STATUSES))
              .filter(models.Candidate.job_title.isnot(None))
              .distinct()
              .all()
        ) if r
    ]
    roles.sort(key=lambda s: s.lower()) # case-insensitive sort

    status_options = sorted(WORKER_STATUSES)

    flash = request.session.pop("flash", None) # One time flash message
    return templates.TemplateResponse( # render the users.html template
        "users.html",
        {
            "request": request,
            "users": users,
            "user_candidates": user_candidates,
            "flash": flash,

            # filter state/choices
            "roles": roles,
            "status_options": status_options,
            "role": role,
            "status": status,
            "date_from": date_from,
            "date_to": date_to,
            "q": q,
        },
    )


# Alias: keep old /admin/staffs working (redirect to canonical /admin/users)
@app.get("/admin/staffs")
def list_staffs_redirect():
    return RedirectResponse(url="/admin/users", status_code=307)


# =========================
# Admin: Training / Assessments / Mixed Views
# =========================
@app.get("/admin/training", response_class=HTMLResponse)
def list_training(request: Request):
    training = []
    return templates.TemplateResponse("training_list.html", {"request": request, "training": training})

@app.get("/admin/candidate-assessment", response_class=HTMLResponse)
def candidate_assessment(request: Request):
    return templates.TemplateResponse("candidate_assessment.html", {"request": request})

@app.get("/admin/candidates-users", response_class=HTMLResponse)
def list_candidates_users(request: Request, db: Session = Depends(get_db)):
    candidates = db.query(models.Candidate).all()
    users = db.query(models.User).all()
    return templates.TemplateResponse(
        "candidates_users.html",
        {"request": request, "candidates": candidates, "users": users},
    )


# =========================
# Admin: Add Employee (create User + Candidate)
# =========================
@app.get("/admin/users/new", response_class=HTMLResponse)
def new_user_form(request: Request):
    return templates.TemplateResponse("user_new.html", {"request": request})

@app.post("/admin/users/new", response_class=HTMLResponse)
def create_user_and_candidate(
    request: Request,
    username: str = Form(...),
    email: EmailStr = Form(...),
    first_name: str = Form(""),
    last_name: str = Form(""),
    job_title: str = Form(""),
    mobile: str = Form(""),
    status: str = Form("Applied"),
    db: Session = Depends(get_db),
):
    existing = db.query(models.User).filter(
        (models.User.username == username) | (models.User.email == email)
    ).first()
    if existing:
        return templates.TemplateResponse(
            "user_new.html",
            {"request": request, "error": "Username or email already exists."},
            status_code=400,
        )

    temp_password = secrets.token_urlsafe(8)
    hashed = hashlib.sha256(temp_password.encode()).hexdigest()  # use your real hasher if available

    user = models.User(username=username, email=email, hashed_password=hashed)
    db.add(user); db.commit(); db.refresh(user)

    cand = models.Candidate(
        first_name=first_name or "",
        last_name=last_name or "",
        email=email,
        mobile=mobile or "",
        job_title=job_title or "",
        status=status or "Applied",
        user_id=user.id,
    )
    db.add(cand); db.commit()

    request.session["flash"] = f"User created. Temporary password: {temp_password}"
    return RedirectResponse(url="/admin/users", status_code=303)


# =========================
# Admin: Applicants (list + convert)
# =========================
@app.get("/admin/applicants", response_class=HTMLResponse)
def list_applicants(request: Request, db: Session = Depends(get_db)):
    applicants = (
        db.query(models.Candidate)
        .filter(~models.Candidate.status.in_(APPLICANT_STATUSES_EXCLUDE))
        .all()
    )
    flash = request.session.pop("flash", None)
    return templates.TemplateResponse("applicants.html", {"request": request, "applicants": applicants, "flash": flash})

@app.get("/admin/applicants/{candidate_id}/profile")
def ensure_profile_and_open(candidate_id: int, request: Request, db: Session = Depends(get_db)):
    cand = db.query(models.Candidate).filter(models.Candidate.id == candidate_id).first()
    if not cand:
        raise HTTPException(status_code=404, detail="Candidate not found")

    # ensure linked user (reuse by id/email, else create)
    user = db.query(models.User).filter(models.User.id == cand.user_id).first() if cand.user_id else None
    if not user and cand.email:
        user = db.query(models.User).filter(models.User.email == cand.email).first()

    if not user:
        base_username = (
            cand.email.split("@")[0] if cand.email and "@" in cand.email
            else f"{(cand.first_name or '').lower()}.{(cand.last_name or '').lower()}".strip(".")
        ) or f"user{cand.id}"

        # ensure unique username
        username = base_username
        i = 1
        while db.query(models.User).filter(models.User.username == username).first():
            i += 1
            username = f"{base_username}{i}"

        temp_password = secrets.token_urlsafe(8)
        hashed = hashlib.sha256(temp_password.encode()).hexdigest()

        user = models.User(
            username=username,
            email=cand.email or f"{username}@example.com",
            hashed_password=hashed,
        )
        db.add(user)
        db.flush()           # get user.id
        cand.user_id = user.id
        db.add(cand)
        db.commit()

        request.session["flash"] = f"Created user '{username}'. Temporary password: {temp_password}"

    return RedirectResponse(url=f"/portal/profile/admin/{user.id}", status_code=303)

# Simple convert (kept for history; overridden below by the robust version)
@app.post("/admin/applicants/{candidate_id}/convert", response_class=HTMLResponse)
def convert_applicant_to_worker(candidate_id: int, request: Request, db: Session = Depends(get_db)):
    cand = db.query(models.Candidate).filter(models.Candidate.id == candidate_id).first()
    if not cand:
        request.session["flash"] = "Candidate not found."
        return RedirectResponse(url="/admin/applicants", status_code=303)

    cand.status = "Hired"
    db.add(cand); db.commit()

    request.session["flash"] = (f"{cand.first_name or ''} {cand.last_name or ''}".strip() or "Candidate") + " moved to Workers."
    return RedirectResponse(url="/admin/users", status_code=303)

# Robust convert (ensures linked User; placed AFTER simple version)
@app.post("/admin/applicants/{candidate_id}/convert", response_class=HTMLResponse)
def convert_applicant_to_worker(candidate_id: int, request: Request, db: Session = Depends(get_db)):
    cand = db.query(models.Candidate).filter(models.Candidate.id == candidate_id).first()
    if not cand:
        request.session["flash"] = "Candidate not found."
        return RedirectResponse(url="/admin/applicants", status_code=303)

    # Ensure the candidate has a linked user
    user = None
    if cand.user_id:
        user = db.query(models.User).filter(models.User.id == cand.user_id).first()

    if not user:
        # Try to reuse existing user by email
        if cand.email:
            user = db.query(models.User).filter(models.User.email == cand.email).first()

        if not user:
            # Create a new user
            base_username = (
                cand.email.split("@")[0] if cand.email and "@" in cand.email
                else f"{(cand.first_name or '').lower()}.{(cand.last_name or '').lower()}".strip(".")
            ) or f"user{cand.id}"

            # Ensure unique username
            username = base_username
            i = 1
            while db.query(models.User).filter(models.User.username == username).first():
                i += 1
                username = f"{base_username}{i}"

            temp_password = secrets.token_urlsafe(8)
            hashed = hashlib.sha256(temp_password.encode()).hexdigest()  # use your normal hasher if you have one

            user = models.User(
                username=username,
                email=cand.email or f"{username}@example.com",
                hashed_password=hashed,
            )
            db.add(user)
            db.flush()  # get user.id without a full commit yet
            # Show the temp password once
            request.session["flash"] = f"Created user '{username}'. Temporary password: {temp_password}"

        cand.user_id = user.id  # link candidate -> user

    # Mark as worker
    cand.status = "Hired"
    db.add(cand)
    db.commit()

    # If user already existed and we didn't set flash above, show a generic message
    if "flash" not in request.session:
        full_name = f"{cand.first_name or ''} {cand.last_name or ''}".strip() or "Candidate"
        request.session["flash"] = f"{full_name} moved to Workers."

    return RedirectResponse(url="/admin/users", status_code=303)


# =========================
# Routers
# =========================
app.include_router(candidates_router.router)
app.include_router(auth_router.router)
app.include_router(portal_router.router)
