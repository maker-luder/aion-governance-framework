"""Evidence preservation after HOLD; all writes restricted to this delivery folder."""
import difflib
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.with_name("aion-governance-reentry-20260910")
BASE = "01676093eaf536e5f449cc099c6a844f9c4ccb84"
INCIDENT = "58ce7c3dae7ac3eefbe89cb659e00dc2f5846b21"
PREFIX = "research-labs/coupled-cognition-quality-factory_v0.1.0/"
DRAFTS = [PREFIX + "src/aion_coupled_quality/reentry_probe.py", PREFIX + "tests/test_governance_reentry.py"]
records = []
env = os.environ.copy()
env["GIT_OPTIONAL_LOCKS"] = "0"


def capture(name, command, cwd=ROOT):
    p = subprocess.run(command, cwd=cwd, env=env, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, encoding="utf-8", errors="replace")
    item = {"name": name, "command": command, "cwd": str(cwd), "output": p.stdout, "exit_status": p.returncode}
    records.append(item)
    print(name, "exit", p.returncode, p.stdout[-500:], flush=True)
    if p.returncode:
        (HERE / "preservation-failure.json").write_text(json.dumps(records, ensure_ascii=False, indent=2), encoding="utf-8")
        raise RuntimeError("HOLD: preservation command failed; no repair attempted")
    return p.stdout


before = capture("candidate_status_before", ["git", "status", "--short", "--untracked-files=all"])
head = capture("candidate_head", ["git", "rev-parse", "HEAD"]).strip()
assert head == BASE
capture("tracked_diff", ["git", "diff", "--exit-code"])
refs = capture("remote_refs", ["git", "ls-remote", "https://github.com/maker-luder/aion-governance-framework.git", "refs/heads/main", "refs/heads/docs/epistemic-workflow-research-20260910"])
assert BASE + "\trefs/heads/main" in refs
assert INCIDENT + "\trefs/heads/docs/epistemic-workflow-research-20260910" in refs

capture("incident_archive", ["git", "archive", "--format=zip", "--output=" + str(HERE / "incident-research-originals.zip"), INCIDENT, "research-notes/human-ai-epistemic-workflow"])
capture("incident_bundle", ["git", "bundle", "create", str(HERE / "incident.bundle"), "refs/remotes/origin/docs/epistemic-workflow-research-20260910"])
capture("incident_bundle_verify", ["git", "bundle", "verify", str(HERE / "incident.bundle")])

draft_bytes = {path: (ROOT / path).read_bytes() for path in DRAFTS}
patch = ""
for path, data in draft_bytes.items():
    patch += f"diff --git a/{path} b/{path}\nnew file mode 100644\n"
    patch += "".join(difflib.unified_diff([], data.decode("utf-8").splitlines(keepends=True), fromfile="/dev/null", tofile="b/" + path))
(HERE / "draft.patch").write_text(patch, encoding="utf-8", newline="\n")
capture("forward_patch_check", ["git", "apply", "--check", str(HERE / "draft.patch")], HERE / "baseline")
capture("reverse_patch_check", ["git", "apply", "--reverse", "--check", str(HERE / "draft.patch")])

with zipfile.ZipFile(HERE / "baseline.zip") as original, zipfile.ZipFile(HERE / "candidate-draft.zip", "w", zipfile.ZIP_DEFLATED) as candidate:
    for info in original.infolist():
        candidate.writestr(info, original.read(info))
    for path, data in draft_bytes.items():
        info = zipfile.ZipInfo(path, (2026, 9, 10, 0, 0, 0))
        info.external_attr = 0o100644 << 16
        candidate.writestr(info, data)

archive_checks = {}
for name in ["baseline.zip", "candidate-draft.zip", "incident-research-originals.zip"]:
    with zipfile.ZipFile(HERE / name) as archive:
        assert archive.testzip() is None
        archive_checks[name] = {"testzip": "PASS", "files": len([i for i in archive.infolist() if not i.is_dir()])}
with zipfile.ZipFile(HERE / "baseline.zip") as original, zipfile.ZipFile(HERE / "candidate-draft.zip") as candidate:
    assert set(candidate.namelist()) - set(original.namelist()) == set(DRAFTS)
    assert all(original.read(p) == candidate.read(p) for p in original.namelist())
    assert all(candidate.read(p) == data for p, data in draft_bytes.items())
    archive_checks["baseline_vs_candidate"] = "SAME_BASELINE_BYTES_PLUS_TWO_DRAFTS"

hashes = {name: hashlib.sha256((HERE / name).read_bytes()).hexdigest() for name in ["baseline.zip", "candidate-draft.zip", "draft.patch", "incident.bundle", "incident-research-originals.zip"]}
(HERE / "archive-hashes.json").write_text(json.dumps(hashes, indent=2), encoding="utf-8")
capture("rollback_read_only", [sys.executable, str(HERE / "rollback.py")], HERE)
capture("rollback_new_copy", [sys.executable, str(HERE / "rollback.py"), "--output", str(HERE / "restored-baseline")], HERE)

source = "docs/history/OWNER_LEARNING_CONTEXT_2026_09_03.md"
raw = subprocess.check_output(["git", "show", BASE + ":" + source], cwd=ROOT, env=env)
disk = (ROOT / source).read_bytes()
byte_evidence = {"path": source, "git_sha256": hashlib.sha256(raw).hexdigest(), "worktree_sha256": hashlib.sha256(disk).hexdigest(), "git_bytes": len(raw), "worktree_bytes": len(disk), "crlf_to_lf_equals_git": disk.replace(b"\r\n", b"\n") == raw}
after = capture("candidate_status_after", ["git", "status", "--short", "--untracked-files=all"])
assert before == after
assert all((ROOT / p).read_bytes() == b for p, b in draft_bytes.items())
capture("final_remote_refs", ["git", "ls-remote", "https://github.com/maker-luder/aion-governance-framework.git", "refs/heads/main", "refs/heads/docs/epistemic-workflow-research-20260910"])

record = {
    "status": "HOLD_PARTIAL_DELIVERY", "baseline": BASE, "incident_head": INCIDENT,
    "candidate_branch": "review/governance-reentry-20260910", "candidate_head": head,
    "baseline_validation": json.loads((HERE / "baseline-verification.json").read_text(encoding="utf-8")),
    "candidate_behavioral_validation": "NOT_PERFORMED_AFTER_HOLD",
    "candidate_draft_syntax": "compileall exit 0 before HOLD; not behavioral validation",
    "preservation_commands": records, "archive_checks": archive_checks,
    "archive_representation": "exact Git baseline bytes plus two untracked draft files; not CRLF worktree image",
    "byte_drift_evidence": byte_evidence,
    "draft_hashes": {p: hashlib.sha256(b).hexdigest() for p, b in draft_bytes.items()},
    "candidate_unchanged_during_preservation": True,
    "new_commits": 0, "remote_mutations": 0, "canonical_effect": "NONE", "deployment": False,
    "capa_effectiveness": "NOT_VERIFIED", "model_id": "UNKNOWN", "reasoning_config": "UNKNOWN",
}
(HERE / "verification.json").write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
reports = list(HERE.glob("*.md"))
for path in reports:
    text = path.read_text(encoding="utf-8")
    assert len(text) > 100 and "\ufffd" not in text
    assert text.count("```") % 2 == 0
print("REPORT_READBACK=PASS", len(reports))
print("PRESERVATION_COMPLETE; CANDIDATE_IMPLEMENTATION_REMAINS_HOLD")
