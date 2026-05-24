# Project context for OpenSpec

OpenSpec uses this file as project-level context. It is read by `openspec validate` and
by any AI tool that respects OpenSpec conventions.

## Project

**Reports app.** A FastAPI app exposing `/reports`. The workshop uses this codebase to
compare three depths of specification.

## Languages and frameworks

Python 3.10+, FastAPI, Pydantic v2, pytest.

## Style conventions

- All public response models suffixed `Public`.
- Internal-only fields (`internal_id`, `owner_email`) MUST NEVER appear in any user-facing
  output.
- CSV output MUST use the standard-library `csv` module and follow RFC 4180.
- Test files use `tests/test_<feature>.py` naming.

## How to propose a change

```bash
openspec change add <change-name>
```

A change directory is created under `openspec/changes/<change-name>/` containing
`proposal.md`, `tasks.md`, and a `specs/` subtree of delta specs. Once implemented and
merged, run:

```bash
openspec archive <change-name>
```

to fold the deltas into `openspec/specs/` and remove the proposal.
