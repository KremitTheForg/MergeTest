# MergeTest Monorepo

This repository now houses both the FastAPI backend and the React (Vite + TypeScript) frontend in a single project tree. The frontend lives inside `backend/frontend` so that builds can be published directly into the backend's static assets.

## Directory layout

- `backend/app` – FastAPI application code
- `backend/frontend` – React SPA source code
- `backend/static` – static assets served by FastAPI (React build artifacts are emitted to `backend/static/forms`)
- `backend/templates` – Jinja templates used as server-rendered fallbacks

## Merging workflow

Follow these steps whenever frontend changes need to be reflected in the backend:

1. **Install frontend dependencies**
   ```bash
   cd backend/frontend
   npm install
   ```

2. **Build the production bundle** (writes into `backend/static/forms` which the backend serves)
   ```bash
   npm run build
   ```

3. **Start the backend** (from the project root)
   ```bash
   uvicorn app.main:app --reload --app-dir backend
   ```

4. Visit `http://localhost:8000/candidate-form`. If a React build exists the FastAPI route serves `backend/static/forms/index.html`; otherwise it falls back to the legacy Jinja `templates/index.html`.

## Local development tips

- Run `npm run dev` inside `backend/frontend` for the Vite dev server while working on React components.
- The backend `@app.get("/candidate-form")` handler automatically detects the built SPA. Regenerate the bundle (`npm run build`) before deploying so the backend serves the latest assets.
- Built assets (`backend/static/forms`) and Node modules are ignored via `.gitignore`; only source changes need to be committed.

## JSON API surface

Most administrative and portal flows now have JSON counterparts under the `/api/v1` prefix. All endpoints reuse the existing session cookie that is set during the HTML login flow, so the easiest way to experiment is to authenticate through the browser first and then reuse the cookies in your API client.

| Endpoint | Description |
| --- | --- |
| `GET /api/v1/me` | Returns the signed-in user plus their linked candidate/profile records (if any). |
| `GET /api/v1/admin/metrics` | High-level counts used by the admin dashboard cards. |
| `GET /api/v1/admin/candidates` | Full candidate list with optional profile/resume metadata. |
| `GET /api/v1/admin/workers` | Worker roster with the same filters that power the HTML view. Accepts `role`, `status`, `date_from`, `date_to`, and `q` query params. |
| `GET /api/v1/admin/applicants` | Applicants that have not been converted into workers yet. |
| `PUT /api/v1/portal/profile` | Updates the signed-in user's profile using a JSON body that mirrors the form fields (summary, skills, linkedin, address, job_title). |
| `POST /api/v1/portal/profile/upload` | Upload resume/photo assets for the current user via multipart form data (`kind` + `file`). |
| `POST /api/v1/hr/recruitment/candidates/` | Existing intake endpoint for creating a candidate (accepts JSON or multipart requests). |

All collection endpoints respond with documented Pydantic schemas (see `backend/app/schemas.py`) so they will also appear in the automatically generated OpenAPI docs at `/docs`.

