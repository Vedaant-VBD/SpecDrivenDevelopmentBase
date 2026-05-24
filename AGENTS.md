# Project context for AI coding tools

Any agent (Cursor, Claude Code, Copilot, Cline, etc.) reading this file is working on the
**Reports API**. Read this before generating any code.

## What this is

A small FastAPI app exposing a `/reports` endpoint. Code quality, security, and adherence
to acceptance criteria matter.

## Stack

- Python 3.10+
- FastAPI + Uvicorn
- Pydantic v2 for models
- pytest for tests
- Pure in-memory data store (`app/data.py`) — no real database

## Project conventions

- Code lives in `app/`. Tests live in `tests/`.
- Public Pydantic response models are named `*Public`; internal/raw models are named `*`.
- **The fields `internal_id` and `owner_email` are internal-only.** They MUST NEVER appear
  in any public API response, CSV export, or other user-facing artifact.
- All new endpoints must be covered by at least one pytest test.
- Use type hints everywhere. Pydantic models for all request/response bodies.
- We follow RFC 4180 strictly for any CSV output.
- We use the standard library `csv` module for CSV serialization, not handwritten escaping.
- Timezone: server times are stored as UTC; user-facing times honor the timezone in the
  `X-User-Timezone` request header, falling back to UTC.

## Things that are out of scope (don't add them)

- Excel (XLSX) export
- PDF export
- Real database / migrations
- Authentication (assume the request is authenticated upstream)
- Scheduled or emailed exports

## How we work with specifications

The directory `openspec/` is the source of truth for what the system is supposed to do.

- `openspec/specs/<capability>/spec.md` is the current spec for each capability.
- `openspec/changes/<change-name>/` is a pending change proposal. It contains a
  `proposal.md`, a `tasks.md`, and one or more delta spec files under `specs/`.
- **Do not modify `openspec/specs/` directly.** Create a change under `openspec/changes/`.

When in doubt: ask for the spec, write the spec, then write the code.
