"""Main FastAPI application entry point.

The bulk of the business logic lives in dedicated routers so that this module
remains focused on application wiring and the small set of shared routes.
"""

from pathlib import Path

from fastapi import Depends, FastAPI, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from starlette.middleware.sessions import SessionMiddleware

from app import models
from app.database import Base, engine, get_db
from app.routers import admin as admin_router
from app.routers import auth as auth_router
from app.routers import candidates as candidates_router
from app.routers import portal as portal_router


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


# =========================
# Public / Authenticated Landing
# =========================
@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    """Render the dashboard for authenticated users or redirect to login."""
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
    """Serve the React-built candidate form when present, otherwise fallback."""
    if FRONTEND_INDEX_FILE.exists():
        return FileResponse(FRONTEND_INDEX_FILE, media_type="text/html")
    return templates.TemplateResponse("index.html", {"request": request})


# =========================
# Routers
# =========================
app.include_router(candidates_router.router)
app.include_router(auth_router.router)
app.include_router(portal_router.router)
app.include_router(admin_router.router)
