from __future__ import annotations

import json
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
LAB_SRC = ROOT / "research-labs" / "csomi-slsh-integration_v0.1.0" / "src"
if str(LAB_SRC) not in sys.path:
    sys.path.insert(0, str(LAB_SRC))

from aion_csomi_slsh_integration.authority import (  # noqa: E402
    assert_authority_semantics,
    load_default_authorities,
)
from aion_csomi_slsh_integration.contract import build_integration_contract  # noqa: E402


OUTPUT = (
    ROOT
    / "research-workbench"
    / "csomi-slsh-integration-2026-08-14"
    / "CSOMI_SLSH_INTEGRATION_RECORD_V0.1.0.json"
)


def main() -> None:
    authorities = load_default_authorities(ROOT)
    for authority in authorities:
        assert_authority_semantics(authority)
    csomi = next(item for item in authorities if item.spec.framework == "CSOMI")
    slsh = next(item for item in authorities if item.spec.framework == "SLSH")
    if slsh.packet.get("base_head") != csomi.spec.authority_sha:
        raise AssertionError(
            "SLSH base_head does not match the pinned CSOMI authority SHA"
        )
    record = build_integration_contract(ROOT, authorities)
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    OUTPUT.write_text(
        json.dumps(record, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    print(
        "CSOMI×SLSH integration materialized: "
        f"authorities={len(authorities)} output={OUTPUT.relative_to(ROOT)}"
    )


if __name__ == "__main__":
    main()
