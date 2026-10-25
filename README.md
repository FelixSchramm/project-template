# project-template

[Copier](https://copier.readthedocs.io/) template for new repositories: one
template for three project types, with an agent-friendly setup (`AGENTS.md`)
and a ready-to-activate autonomous agent relay.

| Project type | What you get |
|---|---|
| `python` | uv, `pyproject.toml`, `src/<package>/`, `tests/`, ruff (format + lint), GitHub Actions CI |
| `analysis` | everything from `python` plus `notebooks/`, `data/` (kept out of git), `ipykernel` |
| `docs` | Markdown only: README, agent files, PR template |

Every type gets `AGENTS.md`, a one-line `CLAUDE.md` (`@AGENTS.md`, because
Claude Code loads `CLAUDE.md`, not `AGENTS.md`), `agents/CODING_RULES.md`,
the dormant relay in `agents/`, a `.gitignore`, an optional MIT license and a
PR template.

## Create a new repository

Requires [uv](https://docs.astral.sh/uv/).

```bash
uvx copier copy gh:FelixSchramm/project-template my-project
cd my-project
git init -b main
uv sync                      # python/analysis only: creates uv.lock for CI
git add . && git commit -m "chore: initial commit from project-template"
git remote add origin https://github.com/FelixSchramm/my-project
git push -u origin main
```

Copier asks for name, description, project type and a few defaults; the
answers are stored in `.copier-answers.yml`.

## Pull in template updates

```bash
uvx copier update --defaults
```

Copier re-applies the template on top of your changes (three-way merge).
Commit or stash first; resolve conflicts like a normal merge.

## Agent setup

```
AGENTS.md                    # project context and pointers, for every agent
CLAUDE.md                    # @AGENTS.md
agents/
  CODING_RULES.md            # coding standards and behavioral guidelines
  RELAY.md                   # agent-neutral relay protocol (worker / reviewer / fallback)
  runtimes/claude-code.md    # how Claude Code cloud sessions start successors
  prompts/                   # kickoff, fallback, optional review phase
docs/handovers/README.md     # archive of handover snapshots
```

The relay lets a chain of single-purpose agent sessions work through a plan
of GitHub issues: a worker implements one issue and opens a PR, a reviewer
reviews, fixes clear findings, merges and starts the next worker; a fallback
task restarts the chain if it stalls. It is **dormant** by default: the files
are present, nothing runs.

Activate it in an existing repository:

```bash
uvx copier update --defaults --data agent_relay=active
```

This marks the relay as active in `AGENTS.md` and creates `HANDOVER.md`,
where the work plan (issue order) goes. The remaining steps (issues,
integration branch, fallback task, kickoff prompt) are listed under
"Activation" in `agents/RELAY.md`.

To use another agent than Claude Code, add an adapter next to
`agents/runtimes/claude-code.md`; `RELAY.md` itself stays unchanged.

## Developing the template

```bash
uv sync
uv run pytest      # renders every project type and runs the generated CI steps
```
