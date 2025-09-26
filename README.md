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

   The backend now defaults to a SQLite database at `backend/app/local.db` if
   no `DATABASE_URL` environment variable is set. This allows the server to boot
   without any additional configuration. To use PostgreSQL or another RDBMS,
   create a `.env` file with `DATABASE_URL=postgresql://user:pass@host/dbname`
   before starting Uvicorn.

4. Visit `http://localhost:8000/candidate-form`. If a React build exists the FastAPI route serves `backend/static/forms/index.html`; otherwise it falls back to the legacy Jinja `templates/index.html`.
   The same SPA bundle now powers `/admin/users/new` and `/portal/profile`, so once the build is in place those pages will render
   the React experience as well.

### Which screens are React-powered?

- **React + Vite SPA** – the public candidate intake flow (`/candidate-form`), the admin “Add Employee” screen (`/admin/users/new`), and the candidate portal profile (`/portal/profile`, `/portal/profile/admin/{user_id}`) are implemented in React. When you run `npm run build` the bundle is emitted to `backend/static/forms` and transparently picked up by the FastAPI routes. During development you can also visit `http://localhost:5173` while running `npm run dev` for hot reload.
- **Server-rendered (Jinja)** – the remaining administrative dashboards (`/admin/...`) and worker management flows outside of “Add Employee” still rely on the legacy templates. They will look identical to the original implementation until they are rewritten in React.

If you are expecting a screen to be React-driven but it still looks like the legacy version, confirm that it lives under the `/candidate-form`, `/admin/users/new`, or `/portal/profile` routes. Anything outside those paths is still backed by the Jinja templates in `backend/templates`.

## Local development tips

- Run `npm run dev` inside `backend/frontend` for the Vite dev server while working on React components.
- The backend `@app.get("/candidate-form")` handler automatically detects the built SPA. Regenerate the bundle (`npm run build`) before deploying so the backend serves the latest assets.
- Built assets (`backend/static/forms`) and Node modules are ignored via `.gitignore`; only source changes need to be committed.

## JSON API surface

Most administrative and portal flows now have JSON counterparts under the `/api/v1` prefix. All endpoints reuse the existing session cookie that is set during the HTML login flow, so the easiest way to experiment is to authenticate through the browser first and then reuse the cookies in your API client.

Refer to [`docs/API.md`](docs/API.md) for a complete endpoint and schema breakdown, including request/response examples and cURL snippets.

All collection endpoints respond with documented Pydantic schemas (see `backend/app/schemas.py`) so they will also appear in the automatically generated OpenAPI docs at `/docs`.

