# Setup — do this BEFORE the workshop starts

Aim to be fully green on the **Setup Check** below ten minutes before kickoff.
If something breaks, ping the facilitator early — don't burn workshop time on Python paths.

## 1. Prerequisites

- **Python 3.10+** — verify with `python3 --version`
- **pip** (comes with Python)
- **Git** — verify with `git --version`
- **Node.js 18+** — only needed for OpenSpec CLI (`node --version`)
- **Cursor** (free tier is fine) — https://cursor.sh
- **A free Anthropic or OpenAI account** — Cursor uses these for the model

## 2. Clone and create a venv

```bash
git clone <this-repo-url> SpecDrivenDevelopmentBase
cd SpecDrivenDevelopmentBase
git checkout 02_openspec

python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

pip install -e ".[dev]"
```

## 3. Smoke-test the app

```bash
# Run the API
uvicorn app.main:app --reload --port 8000
```

In another terminal:

```bash
curl http://localhost:8000/reports?limit=3 | python -m json.tool
```

You should see three report rows back as JSON.

## 4. Run the tests

```bash
pytest -q
```

You should see **all tests pass**. If they don't — stop and ask the facilitator.

## 5. Install OpenSpec CLI

OpenSpec is a tiny CLI for managing spec changes as proposals.

```bash
npm install -g @fission-ai/openspec    # or whatever the OpenSpec install command is for the version pinned in openspec/project.md
openspec --version
```

> If `npm install -g` fails on your machine due to permissions, use a Node version manager
> (nvm, fnm) or run with sudo. Don't burn workshop time debugging npm.

Then verify the project is set up:

```bash
openspec list
```

You should see no pending changes — that's expected. The starter spec lives in
`openspec/specs/reports/spec.md`.

## 6. Cursor setup

1. Open the **`SpecDrivenDevelopmentBase/`** folder in Cursor.
2. Go to **Settings → Models** and confirm you have at least one model available
   (the free tier ships with Claude Haiku and GPT-4.1-mini, either works for the workshop).
3. Open Cursor's **Composer** (Cmd-I / Ctrl-I) and confirm it lists your project files.
4. Open **`AGENTS.md`** in the editor and read it. Cursor will pick this up automatically
   for every prompt you run in this repo.

## Setup-Check checklist

Tick all of these off before kickoff:

- [ ] `uvicorn app.main:app --reload` runs and `/reports` returns JSON
- [ ] `pytest -q` is fully green
- [ ] `openspec list` runs without error
- [ ] Cursor is open on this folder and Composer works
- [ ] You've read `AGENTS.md` and `openspec/project.md`

You're ready. See you at the workshop.
