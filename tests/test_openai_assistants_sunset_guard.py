from __future__ import annotations

import importlib.util
from pathlib import Path


SCRIPT_PATH = Path(__file__).resolve().parents[1] / "scripts" / "audit_openai_assistants_sunset.py"
SPEC = importlib.util.spec_from_file_location("audit_openai_assistants_sunset", SCRIPT_PATH)
assert SPEC is not None and SPEC.loader is not None
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


def test_guard_rejects_deprecated_assistants_sdk(tmp_path: Path) -> None:
    component = tmp_path / "components" / "sample"
    component.mkdir(parents=True)
    (component / "client.py").write_text(
        "client.beta.assistants.create(model='legacy')\n",
        encoding="utf-8",
    )

    report = MODULE.audit(tmp_path)

    assert report["status"] == "FAIL"
    assert any(match["pattern"] == "assistants_sdk" for match in report["matches"])


def test_guard_rejects_legacy_threads_endpoint(tmp_path: Path) -> None:
    component = tmp_path / "components" / "sample"
    component.mkdir(parents=True)
    (component / "client.ts").write_text(
        'fetch("https://api.openai.com/v1/threads/thread_123")\n',
        encoding="utf-8",
    )

    report = MODULE.audit(tmp_path)

    assert report["status"] == "FAIL"
    assert any(match["pattern"] == "legacy_threads_endpoint" for match in report["matches"])


def test_guard_allows_responses_and_conversations(tmp_path: Path) -> None:
    component = tmp_path / "components" / "sample"
    component.mkdir(parents=True)
    (component / "client.py").write_text(
        "client.responses.create(model='gpt-5.6', input='hello')\n"
        "conversation_id = 'conv_123'\n",
        encoding="utf-8",
    )

    report = MODULE.audit(tmp_path)

    assert report["status"] == "PASS"
    assert report["matches"] == []
