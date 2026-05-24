# 00 — Setup check (5 minutes)

Run all four commands below. All four should print success.

```bash
# 1. App boots and serves a request
uvicorn app.main:app --port 8001 &
sleep 2
curl -s http://localhost:8001/health | grep '"ok"'
kill %1

# 2. Tests are green
pytest -q

# 3. OpenSpec is installed and the project is valid
openspec list

# 4. Cursor sees the AGENTS.md
# (no command — open Cursor on this folder and confirm Composer is available)
```

If anything fails, see `SETUP.md` at the repo root and ask the facilitator.
