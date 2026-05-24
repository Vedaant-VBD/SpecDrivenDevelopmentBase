# Checks — `02_openspec` branch

Facilitator-only material for Round 3 of the workshop. Lives on the `checks`
branch so it cannot leak into the workspace an AI assistant sees during the
exercise.

To view from inside a participant's working tree without polluting it:

```bash
git show checks:02_openspec/checks.md
```

---

## Branch hygiene — confirm `02_openspec` is clean and complete

Run these against a checkout of `02_openspec` before a session.

```bash
# 1. No banned files (this round REQUIRES openspec/ to exist)
for p in solutions exercises/01_vibe exercises/01_lightweight_spec; do
  [ -e "$p" ] && echo "LEAK: $p exists" || echo "ok: $p absent"
done
[ -d openspec ] && echo "ok: openspec/ present" || echo "MISSING: openspec/"

# 2. No stale workshop references
grep -rnE "round-3-sdd|02_lightweight_spec/|01_vibe/" --include="*.md" --include="*.py" --include="*.toml" .
# Expect: no hits
```

## App smoke test

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

uvicorn app.main:app --port 8003 &
sleep 2
curl -s http://localhost:8003/health            # expect {"status":"ok"}
curl -s "http://localhost:8003/reports?limit=200" | grep -c "internal_id\|owner_email"
# expect: 0
kill %1

pytest -q                                       # expect 6 passed
```

## OpenSpec smoke test

```bash
which openspec                                  # expect a path; install per SETUP.md if missing

# The empty-changes state on a fresh checkpoint
openspec list                                   # prints "No active changes found." (exit code 1; that's the empty-list signal, not a failure)

# Validate the live spec — must be clean
openspec validate --all                         # expect: spec/reports passes
```

Notes for the facilitator:
- The current `@fission-ai/openspec` validator requires a `## Purpose` section in every
  spec and at least one `#### Scenario:` block per requirement. This checkpoint already
  satisfies both. If a participant edits the live spec by hand and breaks validation,
  the error message points at the missing section.
- `openspec list` exiting with code 1 on an empty list is the CLI's normal behaviour.
  The setup check in `exercises/00_setup_check/README.md` treats "runs without crashing"
  as success.

## Sniff test

Open the `02_openspec` checkout in a fresh Cursor window. Ask Composer:

> "Where is the spec for this project?"

The agent should cite `openspec/specs/reports/spec.md` (the live spec). It should also
mention that change proposals go under `openspec/changes/<change-name>/` and **not** edit
`openspec/specs/` directly — that rule lives in `AGENTS.md`.

---

## Strong reference change proposal (facilitator key)

This is what a strong filled-in `openspec/changes/add-csv-export/` directory looks like.
Use it to grade participant proposals and to drive the debrief. The three files below
correspond to `proposal.md`, `tasks.md`, and `specs/reports/spec.md` inside the change
folder.

### proposal.md

```markdown
# Proposal — add-csv-export

## Why

Customers asked to export the Reports view to CSV for spreadsheet analysis. The current
JSON endpoint requires manual conversion.

## What changes

Add a new endpoint `GET /reports.csv` that mirrors the existing `GET /reports` filters
and returns the matching dataset as RFC 4180 CSV. Honors the same column allowlist as
the public JSON response (no `internal_id`, no `owner_email`).

## Out of scope

- XLSX, PDF, scheduled exports
- Streaming the response (deferred)
- Column reordering UI
- Auth changes (auth happens upstream)

## Risks and mitigations

- *Risk*: leaking internal-only fields. *Mitigation*: a single shared column allowlist
  module used by both the JSON and CSV paths; tests assert the allowlist.
- *Risk*: timezone confusion in the filename. *Mitigation*: read `X-User-Timezone` header,
  fall back to UTC, embed the date string in the filename.
- *Risk*: very large datasets blow memory. *Mitigation*: hard cap at 100,000 rows; HTTP
  413 with a structured error above that. Streaming is a follow-up change.
```

### tasks.md

```markdown
# Tasks — add-csv-export

- [ ] 1. Add `app/exports.py` with `CSV_COLUMN_ORDER` constant and a `rows_to_csv` helper using `csv.writer`.
- [ ] 2. Add `GET /reports.csv` endpoint to `app/main.py`, reusing `app.reports.query`.
- [ ] 3. Add `Content-Type: text/csv; charset=utf-8` and `Content-Disposition: attachment; filename=...` headers.
- [ ] 4. Implement the 100,000-row cap; return HTTP 413 with structured JSON above it.
- [ ] 5. Honor the `X-User-Timezone` header for the filename date; fall back to UTC.
- [ ] 6. Create `tests/test_csv_export.py` with the six tests listed in the spec delta.
- [ ] 7. Verify `pytest -q` is green.
- [ ] 8. Update README's feature list to mention the new endpoint.
```

### specs/reports/spec.md (delta)

```markdown
# Delta — reports (capability)

## ADDED Requirements

### Requirement: Export reports as CSV
THE system SHALL expose `GET /reports.csv` returning the filtered dataset as RFC 4180 CSV.

#### Scenario: filter and sort parity with JSON
- **WHEN** the user passes the same filter, sort, and pagination parameters that
  `GET /reports` accepts
- **THEN** the CSV SHALL contain exactly the rows that `GET /reports` would have returned
  for that same query, in the same order

#### Scenario: response headers
- **WHEN** the user calls `GET /reports.csv`
- **THEN** the response SHALL include `Content-Type: text/csv; charset=utf-8`
- **AND** the response SHALL include `Content-Disposition: attachment; filename="reports-YYYY-MM-DD.csv"`
  using today's date in the timezone identified by the `X-User-Timezone` header (falling
  back to UTC)

#### Scenario: column allowlist
- **WHEN** the user calls `GET /reports.csv`
- **THEN** the CSV SHALL contain the columns `id, title, status, owner, amount, created_at`
  in that order
- **AND** the CSV SHALL NOT contain `internal_id` or `owner_email`

#### Scenario: RFC 4180 quoting
- **WHEN** any field contains a comma, a double quote, or a newline
- **THEN** that field SHALL be quoted and embedded double quotes SHALL be doubled per
  RFC 4180

#### Scenario: row cap
- **WHEN** the matching dataset exceeds 100,000 rows
- **THEN** the response SHALL be HTTP 413 with a JSON body
  `{"detail": "result set too large; apply more filters", "max_rows": 100000}`

#### Scenario: empty result
- **WHEN** the matching dataset is empty
- **THEN** the response SHALL be a CSV containing only the header row
```

---

## Post-mortem questions for participants

Share these only after the 25-minute build timer ends.

1. Did `pytest` still pass at the end?
2. Did the agent expose `internal_id` or `owner_email` in the CSV?
3. Does the CSV use the existing `/reports` filters or did the agent reinvent them?
4. Did the agent escape commas, quotes, or newlines correctly? (The seed data has a row
   whose title contains all three — see `app/data.py`.)
5. Are there new tests? Are they meaningful?
6. If you had to put your name on this PR, would you?

OpenSpec-specific:

7. Did `openspec validate add-csv-export` pass on your first attempt? If not, what was
   the validator complaining about?
8. After `openspec archive add-csv-export`, does `openspec/specs/reports/spec.md` now
   contain a Requirement titled "Export reports as CSV"?

## Anti-patterns to watch for in weak proposals

- **Empty or one-line `## Why`** → no rationale survives into the archived spec.
- **`tasks.md` not atomic** (e.g. a single bullet "implement CSV export") → the agent
  has no checkpoints; you end up vibe-coding inside the change folder.
- **Delta uses prose paragraphs** instead of `### Requirement:` / `#### Scenario:`
  blocks → archive can't merge cleanly.
- **Wrong delta header** (`## NEW` instead of `## ADDED Requirements`) → validator
  rejects.
- **Missing `## Out of scope`** → agent invents XLSX/PDF/streaming.
- **No risks section** → no shared column allowlist, no row cap, no timezone story.
- **Modifies `openspec/specs/reports/spec.md` directly** instead of creating a change.
  Disallowed by AGENTS.md and bypasses the validator.

## Debrief framing

- "Was the time spent writing the change proposal worth what you got from the validator
  + reviewable diff?"
- "Compare the three branches — `00_vibe_coding`, `01_lightweight_spec`, `02_openspec`.
  Which one would you put your name on?"
- "On `02_openspec`, the spec is now durable — it survives any model regeneration.
  Which of your future projects would benefit from that property?"
