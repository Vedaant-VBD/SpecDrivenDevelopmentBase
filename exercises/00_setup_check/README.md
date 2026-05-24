# 00 — Setup check (5 minutes)

Run all three commands below. All three should print success.

```bash
# 1. App boots and serves a request
uvicorn app.main:app --port 8001 &
sleep 2
curl -s http://localhost:8001/health | grep '"ok"'
kill %1

# 2. Tests are green
pytest -q

# 3. Cursor sees the project
# (no command — open Cursor on this folder and confirm Composer is available)
```

If anything fails, see `SETUP.md` at the repo root and ask the facilitator.
