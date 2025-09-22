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

