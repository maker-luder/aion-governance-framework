from __future__ import annotations

from pathlib import Path
from urllib.parse import urlparse

from .enums import Decision, QAStatus
from .models import GateResult, RuntimeSecurityProfile


def _inside(path: Path, root: Path) -> bool:
    try:
        path.resolve().relative_to(root.resolve())
        return True
    except ValueError:
        return False


def check_file_boundary(path: Path, profile: RuntimeSecurityProfile) -> GateResult:
    if any(_inside(path, Path(root)) for root in profile.allowed_roots):
        return GateResult(Decision.ALLOW, (), QAStatus.APPROVED)
    return GateResult(Decision.DENY, ("path is outside approved workspace roots",), QAStatus.QA_HOLD)


def check_network_boundary(url: str, profile: RuntimeSecurityProfile) -> GateResult:
    if profile.network_access == "DENIED_BY_DEFAULT" and not profile.allowed_endpoints:
        return GateResult(Decision.DENY, ("network is denied by default",), QAStatus.QA_HOLD)
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        return GateResult(Decision.DENY, ("invalid network target",), QAStatus.QA_HOLD)
    normalized = f"{parsed.scheme}://{parsed.netloc}"
    if normalized not in profile.allowed_endpoints:
        return GateResult(Decision.DENY, ("endpoint is not explicitly approved",), QAStatus.QA_HOLD)
    return GateResult(Decision.ALLOW, (), QAStatus.APPROVED)


def reject_unsafe_combination(reduced_safeguards: bool, network: bool, credentials: bool, tools: bool) -> GateResult:
    if reduced_safeguards and (network or credentials or tools):
        return GateResult(
            Decision.DENY,
            ("reduced-safeguard models require offline, credential-free, tool-free isolation",),
            QAStatus.REJECTED,
        )
    return GateResult(Decision.ALLOW, (), QAStatus.APPROVED)
