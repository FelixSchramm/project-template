# AGENTS.md

This repository is a [Copier](https://copier.readthedocs.io/) template.
`copier.yml` holds the questions, `template/` the files of a generated
project (`.jinja` files are rendered, conditional names drop files per
project type). `tests/test_template.py` renders every project type.

- Setup: `uv sync`
- Tests: `uv run pytest` (needs network: generated projects run `uv sync`)
- Format and lint: `uv run ruff format .`, `uv run ruff check .`

Rules for changes: keep the template minimal (every file must earn its place
in every generated repo), keep `template/agents/RELAY.md.jinja` agent-neutral
and put agent-specific mechanics into `template/agents/runtimes/`, and follow
`template/agents/CODING_RULES.md.jinja` for this repo too.
