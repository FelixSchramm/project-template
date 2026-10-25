"""Render the template for every project type and check the result."""

import subprocess
from pathlib import Path

import pytest
from copier import run_copy

TEMPLATE = Path(__file__).parent.parent


def render(dst: Path, **data) -> Path:
    data = {"project_name": "Demo Project", "description": "A demo project", **data}
    run_copy(str(TEMPLATE), dst, data=data, defaults=True, vcs_ref="HEAD", quiet=True)
    return dst


@pytest.mark.parametrize("project_type", ["python", "analysis", "docs"])
def test_render(tmp_path, project_type):
    dst = render(tmp_path, project_type=project_type)
    files = {str(p.relative_to(dst)) for p in dst.rglob("*") if p.is_file()}

    assert {"AGENTS.md", "CLAUDE.md", "agents/RELAY.md", "agents/runtimes/claude-code.md", "LICENSE"} <= files
    assert "HANDOVER.md" not in files
    assert ("pyproject.toml" in files) == (project_type != "docs")
    assert ("notebooks/.gitkeep" in files) == (project_type == "analysis")
    for name in files:
        text = (dst / name).read_text()
        assert "{{" not in text and "{%" not in text, name


@pytest.mark.parametrize("project_type", ["python", "analysis"])
def test_generated_project_passes_ci(tmp_path, project_type):
    dst = render(tmp_path, project_type=project_type)
    for cmd in ("uv sync", "uv run ruff format --check .", "uv run ruff check .", "uv run pytest"):
        subprocess.run(cmd.split(), cwd=dst, check=True)


def test_active_relay(tmp_path):
    dst = render(tmp_path, project_type="docs", agent_relay="active")

    assert (dst / "HANDOVER.md").exists()
    assert "**Active.**" in (dst / "AGENTS.md").read_text()
