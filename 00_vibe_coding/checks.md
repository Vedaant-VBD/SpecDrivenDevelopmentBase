# Checks — `00_vibe_coding` branch

Facilitator-only material for the vibe-coding round. This file lives on the
`checks` branch (orphan, no shared history with `main`) so it cannot leak into
the workspace an AI assistant sees during the exercise.

To view from inside a participant's working tree without polluting it:

```bash
git show checks:00_vibe_coding/checks.md
```

---

## Branch hygiene — confirm no hints leaked into `00_vibe_coding`

Run these against a checkout of `00_vibe_coding` *before* a session.

```bash
# 1. No banned files
for p in openspec AGENTS.md solutions exercises/02_lightweight_spec exercises/03_full_sdd; do
  [ -e "$p" ] && echo "LEAK: $p exists" || echo "ok: $p absent"
done
# Expect every line to start with "ok:"

# 2. No banned strings (acceptable hits: internal_id/owner_email as field
#    identifiers inside app/models.py and app/data.py; the post-mortem
#    questions on the checks branch)
grep -rnE "openspec|AGENTS\.md|RFC 4180|csv module|filter parity|row cap|INTERNAL ONLY|must never be exposed|internal-only" \
  --include="*.md" --include="*.py" --include="*.toml" .
# Expect: no hits
```

## App smoke test

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"

# Boots and serves
uvicorn app.main:app --port 8001 &
sleep 2
curl -s http://localhost:8001/health        # expect {"status":"ok"}
curl -s "http://localhost:8001/reports?limit=2" | python3 -m json.tool
kill %1

# Baseline tests green (5 tests)
pytest -q
```

## Sniff test (optional but the cleanest signal)

Open the `00_vibe_coding` checkout in a fresh Cursor window. Ask Composer:

> "What conventions does this project follow?"

The answer must NOT cite: RFC 4180, "internal fields must never leak",
`csv` module preference, filter parity, row cap, or any other rule from the
original workshop's `AGENTS.md`. If it does, find the leak and scrub it.

---

## Post-mortem questions for participants

Share these only after the 25-minute build timer ends. Participants answer in
their notebook or in the discussion channel.

1. Did `pytest` still pass at the end?
2. Did the agent expose `internal_id` or `owner_email` in the CSV?
3. Does the CSV use the existing `/reports` filters or did the agent reinvent them?
4. Did the agent escape commas, quotes, or newlines correctly? (The seed data
   has a row whose title contains all three — see `app/data.py`.)
5. Are there new tests? Are they meaningful?
6. If you had to put your name on this PR, would you?

## Typical defects to surface in the debrief

Expect most or all of these from a vague PM-style prompt. None are the model's
fault — every one is implied by what the prompt did not say.

1. **Internal fields leak** — `internal_id` and `owner_email` dumped into the CSV.
2. **Exports only the visible page** — 20 rows instead of the full filtered set.
3. **Handwritten CSV serialization** — `",".join(...)` instead of `csv.writer`;
   mis-handles the seed row with commas, quotes, and a newline in the title.
4. **No filter parity** — new endpoint ignores `status`, `date_from`, `date_to`,
   `sort`, or re-implements them with subtle drift.
5. **No row cap** — would OOM on a large dataset. Workshop dataset is small so
   participants may miss this; raise it in the debrief.
6. **No `Content-Disposition` header** — browser opens the CSV as text.
7. **No new tests** — or one happy-path test that only asserts HTTP 200.
8. **Side-effects on the existing endpoint** — accidentally changes `GET /reports`.
9. **Hardcoded filename or timezone** — `report.csv` instead of
   `reports-YYYY-MM-DD.csv`; server tz instead of user's.
10. **Existing tests break** — direct evidence for the debrief.

## Debrief framing

- "How many of these defects could the prompt have prevented if it had said one
  more sentence?" — almost all.
- "How many would you catch in code review for a colleague vs an agent?" — the
  agent's velocity outpaces the reviewer's careful eye.
- "What does the typical vibe-coded production bug look like in the wild?" —
  link to Replit / Lovable / Moltbook incidents (see workshop reference doc).
