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
npm install -g @fission-ai/openspec@1.2.0
openspec --version    # expect: 1.2.0
```

> The workshop is pinned to **OpenSpec 1.2.0**. Other versions may have stricter
> validators or different folder layouts and can break the exercise mid-flight.

> If `npm install -g` fails on your machine due to permissions, use a Node version manager
> (nvm, fnm) or run with sudo. Don't burn workshop time debugging npm.

Then verify the project is set up:

```bash
openspec list
```

You should see "No active changes found." — that's expected (the CLI exits with code 1
on an empty list; treat "runs without crashing" as success). The starter spec lives in
`openspec/specs/reports/spec.md`.

## 6. IDE setup — pick the one you use

This branch ships with OpenSpec already initialized for four editors. The
slash commands and skills live in the per-editor folders below; **you do not
need to run `openspec init` yourself**. Pick the section that matches your
editor.

After opening the project, **restart the IDE once** so the slash commands and
skills are picked up.

### 6a. Cursor

1. Open the **`SpecDrivenDevelopmentBase/`** folder in Cursor.
2. Settings → Models: confirm at least one model is available.
3. Open Composer (Cmd-I / Ctrl-I). Cursor automatically loads:
   - **Slash commands** from `.cursor/commands/`: `/opsx-propose`, `/opsx-apply`,
     `/opsx-archive`, `/opsx-explore`.
   - **Skills** from `.cursor/skills/`: `openspec-propose`, `openspec-apply-change`,
     `openspec-archive-change`, `openspec-explore`.
   - **`AGENTS.md`** as ambient context.

### 6b. Claude Code

1. Open the folder in Claude Code (`claude` in the terminal, or the IDE extension).
2. Slash commands live under `.claude/commands/opsx/`. Invoke them with the
   namespaced form: `/opsx:propose`, `/opsx:apply`, `/opsx:archive`, `/opsx:explore`.
3. Skills live under `.claude/skills/`. Claude auto-discovers them; reference them
   by name or let the model pick.
4. `AGENTS.md` is read automatically (Claude Code picks up `AGENTS.md` or
   `CLAUDE.md` at the repo root).

### 6c. Antigravity

1. Open the folder in Antigravity.
2. The agent reads `.agent/skills/` for skills and `.agent/workflows/` for
   workflow definitions (`opsx-propose`, `opsx-apply`, `opsx-archive`, `opsx-explore`).
3. Invoke workflows by name in the agent prompt: "run the opsx-propose workflow".

### 6d. VS Code (GitHub Copilot)

1. Open the folder in VS Code with the GitHub Copilot extension installed and enabled.
2. Copilot reads `.github/prompts/` for slash-style prompt files: `opsx-propose.prompt.md`,
   `opsx-apply.prompt.md`, `opsx-archive.prompt.md`, `opsx-explore.prompt.md`.
3. Skills live under `.github/skills/`; reference them from your Copilot Chat
   messages.
4. Copilot also reads `AGENTS.md` as repo-level context.

### What each command does

| Command | What it does |
| --- | --- |
| `opsx-propose` (or `/opsx:propose`) | Start a new change proposal from a natural-language idea. Creates `openspec/changes/<name>/{proposal.md, tasks.md, specs/...}` skeletons. |
| `opsx-explore` | Walk the current spec(s) and the proposal so the agent has full context before coding. |
| `opsx-apply` | Implement the change task-by-task against the codebase. |
| `opsx-archive` | Validate the change, fold the delta into `openspec/specs/`, and remove the proposal. |

## Setup-Check checklist

Tick all of these off before kickoff:

- [ ] `uvicorn app.main:app --reload` runs and `/reports` returns JSON
- [ ] `pytest -q` is fully green
- [ ] `openspec --version` prints `1.2.0`
- [ ] `openspec list` runs and prints "No active changes found."
- [ ] Your IDE is open on this folder; slash commands / skills appear in the agent UI
- [ ] You've read `AGENTS.md` and `openspec/project.md`

You're ready. See you at the workshop.
