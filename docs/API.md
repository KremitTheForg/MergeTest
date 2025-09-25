# API Reference

This document summarizes the JSON APIs that ship with the FastAPI backend. The
backend sets a signed session cookie when a user signs in through the HTML
login form at `/auth/login`. All endpoints in this document expect that cookie
for authentication unless noted otherwise.

- **Base URL:** `/api/v1`
- **Authentication:** browser session cookie issued by the HTML login flow.

> Tip: Sign into the app with your browser first, then copy the session cookie
> (`session`) into an API client such as Hoppscotch or Insomnia.

## Identity

### `GET /api/v1/me`
Returns the currently authenticated user and any linked candidate/profile data.

**Response:**

| Field | Type | Notes |
| --- | --- | --- |
| `user` | [`UserOut`](#userout) | Always present. |
| `candidate` | [`CandidateOut`](#candidateout) \| `null` | Present when the user has a candidate row. |
| `profile` | [`CandidateProfileOut`](#candidateprofileout) \| `null` | Present when the candidate has profile data or uploads. |

## Admin dashboards

All admin endpoints reuse the filters and data that power the HTML admin pages.
They are read-only and require an authenticated session.

### `GET /api/v1/admin/metrics`
Aggregated counts for the dashboard hero cards.

**Response:** [`AdminMetrics`](#adminmetrics)

### `GET /api/v1/admin/candidates`
Full candidate list together with resume/profile metadata.

**Response:**

| Field | Type | Notes |
| --- | --- | --- |
| `results` | [`CandidateWithProfile[]`](#candidatewithprofile) | Ordered by creation time (newest first). |

### `GET /api/v1/admin/workers`
Returns the worker roster using the same filters as the HTML view.

**Query parameters:**

| Name | Type | Description |
| --- | --- | --- |
| `role` | string | Filter by job role slug. |
| `status` | string | Filter by worker status bucket. |
| `date_from` | `YYYY-MM-DD` | Only include candidates converted on or after this date. |
| `date_to` | `YYYY-MM-DD` | Only include candidates converted on or before this date. |
| `q` | string | Free-text search across name, email, and phone. |

**Response:**

| Field | Type | Notes |
| --- | --- | --- |
| `results` | [`WorkerUserOut[]`](#workeruserout) | Ordered exactly as the HTML table. |
| `filters` | [`WorkerQueryFilters`](#workerqueryfilters) | Echoes the normalized filter state. |
| `roles` | `string[]` | All available role filter options. |
| `status_options` | `string[]` | All available status filter options. |

### `GET /api/v1/admin/applicants`
Applicants that have not yet been converted into workers.

**Response:**

| Field | Type | Notes |
| --- | --- | --- |
| `results` | [`CandidateOut[]`](#candidateout) | |

## Candidate intake

### `POST /api/v1/hr/recruitment/candidates/`
Creates a new candidate record. The endpoint accepts either JSON or multipart
form data and automatically links the new candidate to the logged-in user when
their email addresses match.

**Request (JSON example):**
```json
{
  "first_name": "Taylor",
  "last_name": "Doe",
  "email": "taylor@example.com",
  "mobile": "+1 555-123-4567",
  "job_title": "Field Technician",
  "address": "123 Main St, Springfield",
  "applied_on": "2024-05-01"
}
```

**Request (multipart form):**

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `first_name` | text | ✓ | |
| `last_name` | text | ✓ | |
| `email` | text | ✓ | |
| `mobile` | text |  | Optional phone number. |
| `job_title` | text |  | Optional role of interest. |
| `address` | text |  | Optional mailing address. |
| `applied_on` | text |  | `YYYY-MM-DD`. Stored as UTC midnight. |
| `resume` | file |  | Optional resume upload. Saved under `/uploads/{candidate_id}`. |

**Responses:**

- `201 Created` – JSON body: `{ "id": <candidate_id>, "detail": "created", "resume_uploaded": <bool> }`
- `401 Unauthorized` – user is not signed in.
- `409 Conflict` – a candidate with the same email already exists.
- `422 Unprocessable Entity` – invalid payload (validation errors listed in `detail`).

## Candidate portal

### `PUT /api/v1/portal/profile`
Updates the signed-in candidate's profile information.

**Request body:** [`ProfileUpdatePayload`](#profileupdatepayload). All fields are
optional; omitted fields are left unchanged. Setting a field to an empty string
will clear it in the database.

**Response:** [`ProfileResponse`](#profileresponse)

### `POST /api/v1/portal/profile/upload`
Uploads resume or photo assets for the signed-in candidate.

**Multipart fields:**

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `kind` | text | ✓ | Either `resume`, `photo`, or `picture` (alias for `photo`). |
| `file` | file | ✓ | Binary file contents. |

**Response:** [`ProfileUploadResponse`](#profileuploadresponse)

## Shared schema definitions

### `UserOut`
```json
{
  "id": 1,
  "username": "taylorsmith",
  "email": "taylor@example.com"
}
```

### `CandidateOut`
```json
{
  "id": 42,
  "first_name": "Taylor",
  "last_name": "Doe",
  "email": "taylor@example.com",
  "mobile": "+1 555-123-4567",
  "job_title": "Field Technician",
  "address": "123 Main St, Springfield",
  "status": "Applied",
  "applied_on": "2024-05-01T00:00:00Z"
}
```

### `CandidateProfileOut`
```json
{
  "id": 10,
  "summary": "Experienced field tech...",
  "skills": "Electrical, OSHA",
  "linkedin": "https://www.linkedin.com/in/taylor",
  "address": "123 Main St, Springfield",
  "resume_path": "uploads/42/resume.pdf",
  "photo_path": "uploads/42/photo.jpg"
}
```

### `CandidateWithProfile`
```json
{
  "candidate": { /* CandidateOut */ },
  "profile": { /* CandidateProfileOut */ }
}
```

### `WorkerUserOut`
```json
{
  "user": { /* UserOut */ },
  "candidate": { /* CandidateOut */ }
}
```

### `WorkerQueryFilters`
```json
{
  "role": "field-tech",
  "status": "Active",
  "date_from": "2024-01-01",
  "date_to": "2024-06-30",
  "q": "Taylor"
}
```

### `AdminMetrics`
```json
{
  "candidates": 125,
  "users": 87,
  "training": 14
}
```

### `ProfileUpdatePayload`
```json
{
  "summary": "Updated summary",
  "skills": "Electrical, OSHA",
  "linkedin": "https://www.linkedin.com/in/taylor",
  "address": "456 Elm St, Springfield",
  "job_title": "Senior Field Technician"
}
```

### `ProfileResponse`
```json
{
  "candidate": { /* CandidateOut */ },
  "profile": { /* CandidateProfileOut */ }
}
```

### `ProfileUploadResponse`
```json
{
  "candidate_id": 42,
  "kind": "resume",
  "path": "uploads/42/resume.pdf"
}
```

## Testing the endpoints quickly

```
# after logging in via the browser, copy the session cookie
curl -H "Cookie: session=<value>" http://localhost:8000/api/v1/me
```

For multipart uploads, use `curl -F`:

```
curl -X POST \
  -H "Cookie: session=<value>" \
  -F "kind=resume" \
  -F "file=@/path/to/resume.pdf" \
  http://localhost:8000/api/v1/portal/profile/upload
```

