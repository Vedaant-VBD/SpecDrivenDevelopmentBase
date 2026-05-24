# Checks — `01_lightweight_spec` branch

Facilitator-only material for Round 2 of the workshop. Lives on the `checks`
branch so it cannot leak into the workspace an AI assistant sees during the
exercise.

To view from inside a participant's working tree without polluting it:

```bash
git show checks:01_lightweight_spec/checks.md
```

---

## Branch hygiene — confirm `01_lightweight_spec` is clean

Run these against a checkout of `01_lightweight_spec` before a session.

```bash
# 1. No banned files
for p in openspec solutions exercises/01_vibe exercises/03_full_sdd; do
  [ -e "$p" ] && echo "LEAK: $p exists" || echo "ok: $p absent"
done
# Expect every line to start with "ok:"

# 2. No openspec / other-round references in any tracked file
grep -rnE "openspec|round-2|03_full_sdd" --include="*.md" --include="*.py" --include="*.toml" .
# Expect: no hits

# 3. AGENTS.md still carries the conventions but does NOT mention openspec
grep -nE "internal_id|RFC 4180|csv" AGENTS.md   # expect hits
grep -n  "openspec" AGENTS.md                   # expect no hits
```

## App smoke test

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

uvicorn app.main:app --port 8002 &
sleep 2
curl -s http://localhost:8002/health            # expect {"status":"ok"}
curl -s "http://localhost:8002/reports?limit=2" | python3 -m json.tool
kill %1

pytest -q                                       # expect 6 tests, all passing
```

## Sniff test

Open the `01_lightweight_spec` checkout in a fresh Cursor window. Ask Composer:

> "What conventions does this project follow?"

Unlike the vibe round, the answer **should** cite RFC 4180, the internal_id
non-leak rule, the `csv` module preference, and the out-of-scope list — because
`AGENTS.md` is included on this branch. That ambient context is the round's
baseline. The participant's spec sits on top of it.

---

## Strong reference spec (facilitator key)

This is what a strong filled-in `SPEC_TEMPLATE.md` looks like. Use it to grade
participant specs and to drive the debrief.

```markdown
# Spec — Reports CSV export (v0.1)

## What

A user can download, as a CSV file, the report dataset currently filtered and sorted on
the Reports page — honoring filters, sort, and column visibility.

## Acceptance criteria

- WHEN the user calls `GET /reports.csv` with the same filter parameters as `GET /reports`
  THE SYSTEM SHALL return the same rows that `GET /reports` would have returned, but
  exported as CSV instead of JSON.
- THE response SHALL have `Content-Type: text/csv; charset=utf-8`.
- THE response SHALL have `Content-Disposition: attachment; filename="reports-YYYY-MM-DD.csv"`
  using today's date in the user's timezone (header `X-User-Timezone`, fallback UTC).
- THE CSV SHALL contain the columns `id, title, status, owner, amount, created_at` in
  that order. It SHALL NOT contain `internal_id` or `owner_email`.
- THE CSV SHALL conform to RFC 4180 quoting rules; use Python's stdlib `csv` module.
- WHEN the matching dataset exceeds 100,000 rows THE SYSTEM SHALL respond HTTP 413 with
  a JSON body `{"detail": "result set too large; apply more filters", "max_rows": 100000}`.
- WHEN the matching dataset is empty THE SYSTEM SHALL still return a valid CSV
  containing only the header row.

## Out of scope

- XLSX / PDF export
- Scheduled or emailed exports
- Streaming for very large datasets (later)
- Column reordering UI

## Tests required

- `tests/test_csv_export.py`
  - returns 200 with `text/csv` content type and an `attachment` Content-Disposition
  - column order is exactly id, title, status, owner, amount, created_at
  - never contains `internal_id` or `owner_email`
  - status filter parity with `/reports`
  - the seed row with commas, quotes, and a newline in the title is quoted per RFC 4180
  - empty filter result returns the header row only

## Notes

- Reuse `app.reports.query` for filtering — do not re-implement.
- Use stdlib `csv.writer` only; do not write your own escaping.
```

---

## Post-mortem questions for participants

Share these only after the 20-minute build timer ends.

1. Did `pytest` still pass at the end?
2. Did the agent expose `internal_id` or `owner_email` in the CSV?
3. Does the CSV use the existing `/reports` filters or did the agent reinvent them?
4. Did the agent escape commas, quotes, or newlines correctly? (The seed data has a row
   whose title contains all three — see `app/data.py`.)
5. Are there new tests? Are they meaningful?
6. If you had to put your name on this PR, would you?

## Anti-patterns to watch for in weak specs

- **One-liner "What"** with no acceptance criteria → agent invents the contract.
- **Imperatives instead of falsifiable statements** ("Should be fast", "Should be robust")
  → no test can disprove it.
- **No "out of scope"** → agent adds Excel/PDF/streaming because the PM message hinted
  at "downloads."
- **No filename / Content-Disposition expectations** → browser opens CSV as text.
- **No row cap** → no 413 path; OOM-prone on large datasets.
- **No timezone language** → agent uses server local for the filename date.
- **Tests required is vague** ("add tests") → agent writes a single happy-path test.
- **Doesn't reuse `app.reports.query`** → filter logic diverges from `/reports`.

## Debrief framing

- "How many of these defects could one more acceptance-criteria line have prevented?"
- "Where did your spec just duplicate what `AGENTS.md` already says? Where did it add
  real new constraints?"
- "If you had handed this spec to a colleague instead of an agent, would they have
  asked clarifying questions? Which ones?"
