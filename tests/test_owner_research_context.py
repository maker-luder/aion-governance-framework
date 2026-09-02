import hashlib
import json
from pathlib import Path
import shutil
import sys

import pytest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from read_owner_research_context import RECORD, SOURCE, TASK, read_context


@pytest.fixture
def reference_root(tmp_path):
    for relative in (RECORD, SOURCE, Path("schemas/governed_knowledge_source_v0.1.0.schema.json")):
        path = tmp_path / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(ROOT / relative, path)
    return tmp_path


@pytest.mark.parametrize("agent", ["AION", "ASTRA"])
def test_explicit_read_is_attributed_and_bounded(agent):
    result = read_context(agent=agent, task=TASK)
    assert "並不是拋棄" in result["text"]
    assert result["bytes"] <= result["context_byte_cap"] == 4096
    assert result["canonical_effect"] == "NONE"
    assert result["writeback_authority"] == "NONE"
    assert result["subjectivity"] == "NOT_ESTABLISHED"
    assert result["attribution"] == "HUMAN_OWNER_REPORTED_NOT_INTERNAL_AGENT_MEMORY"


@pytest.mark.parametrize("agent,task", [("UNKNOWN", TASK), ("AION", "EXECUTE"), ("ASTRA", "")])
def test_unrequested_or_unlisted_read_rejected(agent, task):
    with pytest.raises(ValueError, match="allowlisted"):
        read_context(agent=agent, task=task)


def test_source_tampering_rejected(reference_root):
    (reference_root / SOURCE).write_text("changed", encoding="utf-8")
    with pytest.raises(ValueError, match="hash mismatch"):
        read_context(agent="AION", task=TASK, root=reference_root)


@pytest.mark.parametrize("key,value", [
    ("registry_status", "CANDIDATE"), ("authority_level", "OPERATIONAL_INPUT_ONLY"),
    ("provenance", {"kind": "REPOSITORY_FILE", "locator": "../outside.md"}),
    ("allowed_tasks", ["EXECUTE"]), ("context_token_cap", 10000),
])
def test_profile_drift_rejected(reference_root, key, value):
    path = reference_root / RECORD
    record = json.loads(path.read_text(encoding="utf-8"))
    record[key] = value
    path.write_text(json.dumps(record), encoding="utf-8")
    with pytest.raises(ValueError, match="profile changed"):
        read_context(agent="ASTRA", task=TASK, root=reference_root)


def test_oversized_source_rejected_even_with_matching_hash(reference_root):
    content = b"x" * 4097
    (reference_root / SOURCE).write_bytes(content)
    path = reference_root / RECORD
    record = json.loads(path.read_text(encoding="utf-8"))
    record["content_hash"] = "sha256:" + hashlib.sha256(content).hexdigest()
    path.write_text(json.dumps(record), encoding="utf-8")
    with pytest.raises(ValueError, match="budget"):
        read_context(agent="AION", task=TASK, root=reference_root)
