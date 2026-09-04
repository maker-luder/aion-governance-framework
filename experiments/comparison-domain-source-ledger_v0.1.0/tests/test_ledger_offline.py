from __future__ import annotations

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(HERE))

from run_experiment import run  # noqa: E402


def test_narrow_claims_do_not_use_network_and_keep_holds() -> None:
    report = run(write_derived=False)
    assert report["network_used"] is False
    assert report["paid_api_used"] is False
    assert report["SUBJECTIVITY_CONCLUSION"] == "NOT_ESTABLISHED"
    assert report["SUBJECTIVITY_EVIDENCE_WEIGHT"] == 0
    assert report["CANONICAL_EFFECT"] == "NONE"
    assert report["DEPLOYMENT"] is False
    assert report["LEDGER_AUTHORITY"] == "NONE_DERIVED_REPORT_ONLY"
    by_claim = {item["claim"]: item["result"] for item in report["claims"]}
    assert by_claim["C1_REGISTER_FILES_PARSE_WITH_SOURCES_ARRAY"] == "SUPPORTED"
    assert by_claim["C2_LICENSE_OR_USAGE_METADATA_PRESENT"] == "SUPPORTED"
    assert by_claim["C3_CHECKED_IN_CONTENT_HASH_RECOMPUTES"] in {
        "SUPPORTED",
        "PARTIALLY_SUPPORTED",
        "NOT_SUPPORTED",
    }
    assert report["aggregate_of_narrow_claims"] in {
        "SUPPORTED",
        "PARTIALLY_SUPPORTED",
        "NOT_SUPPORTED",
    }
    # C3 may be PARTIALLY_SUPPORTED when a recorded repository_sha256
    # no longer matches the working tree. That is a result, not a hidden pass.


def test_hash_only_entries_are_not_applicable() -> None:
    report = run(write_derived=False)
    skipped = report["claims"][2]["skipped_not_applicable"]
    assert skipped
    assert all(row["local_hash"] == "NOT_APPLICABLE" for row in skipped)


def test_result_json_is_json_serializable() -> None:
    report = run(write_derived=False)
    json.dumps(report)
