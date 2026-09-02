"""Read one governed, source-attributed Owner reference on explicit demand only."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE = Path("docs/history/OWNER_LEARNING_CONTEXT_2026_09_03.md")
RECORD = Path("docs/research/sources/owner-learning-context.json")
TASK = "OWNER_LEARNING_HISTORY"


def read_context(*, agent: str, task: str, root: Path = ROOT) -> dict[str, object]:
    import jsonschema

    if agent not in {"AION", "ASTRA"} or task != TASK:
        raise ValueError("reference requires an allowlisted agent and task")
    root = root.resolve()
    paths = [root / RECORD, root / SOURCE]
    for path in paths:
        if path.is_symlink() or root not in path.resolve().parents:
            raise ValueError("reference path escapes repository or is a symlink")
    record = json.loads(paths[0].read_text(encoding="utf-8"))
    schema = json.loads((root / "schemas/governed_knowledge_source_v0.1.0.schema.json").read_text(encoding="utf-8"))
    jsonschema.Draft202012Validator(schema).validate(record)
    expected = {
        "source_id": "owner-learning-context-2026-09-03",
        "registry_status": "ACTIVE_REFERENCE", "epistemic_role": "REFERENCE",
        "verification_policy": "SOURCE_GROUNDED", "freshness_policy": "VERSION_BOUND",
        "authority_level": "REFERENCE_ONLY", "context_token_cap": 4096,
        "allowed_agents": ["AION", "ASTRA"], "allowed_tasks": [TASK],
        "provenance": {"kind": "REPOSITORY_FILE", "locator": SOURCE.as_posix()},
    }
    if any(record.get(key) != value for key, value in expected.items()):
        raise ValueError("governed reference profile changed")
    with paths[1].open("rb") as stream:
        payload = stream.read(4097)
    if len(payload) > 4096:
        raise ValueError("reference exceeds the fixed 4096-byte budget")
    digest = "sha256:" + hashlib.sha256(payload).hexdigest()
    if digest != record["content_hash"]:
        raise ValueError("reference content hash mismatch")
    return {
        "agent": agent, "task": task, "source_id": record["source_id"],
        "source_path": SOURCE.as_posix(), "content_hash": digest,
        "text": payload.decode("utf-8"), "bytes": len(payload),
        "context_policy": "ON_DEMAND", "context_byte_cap": 4096,
        "attribution": "HUMAN_OWNER_REPORTED_NOT_INTERNAL_AGENT_MEMORY",
        "authority_level": "REFERENCE_ONLY", "writeback_authority": "NONE",
        "canonical_effect": "NONE", "deployment": False,
        "subjectivity": "NOT_ESTABLISHED",
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--agent", required=True, choices=["AION", "ASTRA"])
    parser.add_argument("--task", required=True, choices=[TASK])
    args = parser.parse_args()
    print(json.dumps(read_context(agent=args.agent, task=args.task), ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
