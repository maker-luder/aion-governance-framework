from pathlib import Path
import re

ROOT = Path(__file__).resolve().parents[1]


def test_every_remote_action_is_pinned_to_an_exact_commit():
    references = []
    for path in (ROOT / ".github/workflows").glob("*.yml"):
        for reference in re.findall(r"(?m)^\s*(?:-\s*)?uses:\s*([^\s#]+)", path.read_text()):
            if reference.startswith("./"):
                continue
            references.append(reference)
            assert re.fullmatch(r"[\w.-]+/[\w./-]+@[0-9a-f]{40}", reference), (path.name, reference)
    assert references


def test_quality_runs_entire_root_suite_and_offline_research_verification():
    workflow = (ROOT / ".github/workflows/quality.yml").read_text()
    assert "run: python -m pytest -q tests\n" in workflow
    assert "run: python scripts/fetch_subjectivity_sources.py\n" in workflow
    assert 'python-version: ["3.11", "3.12"]' in workflow
