from __future__ import annotations

from dataclasses import asdict, dataclass
from enum import Enum
from hashlib import sha256
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
from typing import Iterable

from .core import InquiryReport


class HarnessExecutionClass(str, Enum):
    STATE_LEVEL = "STATE_LEVEL"
    MODEL_LEVEL = "MODEL_LEVEL"


class HarnessExecutionStatus(str, Enum):
    EXECUTED = "EXECUTED"
    REJECTED = "REJECTED"
    FAILED = "FAILED"


@dataclass(frozen=True)
class HarnessRegistration:
    harness_id: str
    lab_path: str
    entrypoint: str
    python_source: str
    execution_class: HarnessExecutionClass
    enabled: bool
    network_access: bool = False
    secret_access: bool = False
    repository_mutation: bool = False
    deployment: bool = False
    canonical_effect: str = "NONE"
    live_model_execution: bool = False

    def __post_init__(self) -> None:
        if not self.harness_id.strip():
            raise ValueError("harness_id must not be empty")
        for value in (self.lab_path, self.entrypoint, self.python_source):
            if not value.strip() or Path(value).is_absolute() or ".." in Path(value).parts:
                raise ValueError("harness paths must be normalized repository-relative paths")
        if not self.lab_path.startswith("research-labs/"):
            raise ValueError("harness lab_path must remain under research-labs")
        if not self.entrypoint.startswith(self.lab_path + "/"):
            raise ValueError("harness entrypoint must remain inside its registered lab")
        if not self.python_source.startswith(self.lab_path + "/"):
            raise ValueError("harness python source must remain inside its registered lab")
        if self.network_access or self.secret_access or self.repository_mutation or self.deployment:
            raise ValueError("registered autonomous harnesses must be read-only, credential-free, and non-deploying")
        if self.canonical_effect != "NONE":
            raise ValueError("harness canonical_effect must remain NONE")
        if self.execution_class is HarnessExecutionClass.MODEL_LEVEL and self.enabled:
            raise ValueError("live model-level harness execution is not enabled in this profile")
        if self.live_model_execution and self.execution_class is not HarnessExecutionClass.MODEL_LEVEL:
            raise ValueError("live_model_execution requires MODEL_LEVEL execution class")


@dataclass(frozen=True)
class HarnessExecutionReceipt:
    harness_id: str
    execution_class: HarnessExecutionClass
    status: HarnessExecutionStatus
    requested_by: str
    repository_ref: str
    entrypoint_ref: str
    entrypoint_sha256: str
    registration_sha256: str
    result_sha256: str
    receipt_sha256: str
    state_intervention_observed: bool
    live_model_execution: bool
    network_access: bool
    secret_access: bool
    repository_mutation: bool
    deployment: bool
    canonical_effect: str
    observation: str
    follow_up_question: str
    result_payload: dict[str, object]
    stderr_excerpt: str = ""


class HarnessRegistry:
    def __init__(self, registrations: Iterable[HarnessRegistration]) -> None:
        values = tuple(registrations)
        ids = [item.harness_id for item in values]
        if len(ids) != len(set(ids)):
            raise ValueError("harness registry contains duplicate harness ids")
        self._registrations = values
        self._by_id = {item.harness_id: item for item in values}

    @property
    def registrations(self) -> tuple[HarnessRegistration, ...]:
        return self._registrations

    def resolve(self, harness_id: str) -> HarnessRegistration:
        try:
            return self._by_id[harness_id]
        except KeyError as exc:
            raise ValueError(f"unknown research harness: {harness_id}") from exc

    def recommend_for_report(self, report: InquiryReport, *, limit: int = 2) -> tuple[str, ...]:
        if limit <= 0:
            return ()
        evidence_refs = "\n".join(item.ref for item in report.evidence)
        chosen: list[str] = []
        for registration in self._registrations:
            if not registration.enabled:
                continue
            if registration.execution_class is not HarnessExecutionClass.STATE_LEVEL:
                continue
            if registration.lab_path in evidence_refs:
                chosen.append(registration.harness_id)
                if len(chosen) >= limit:
                    break
        return tuple(chosen)


def default_harness_registry() -> HarnessRegistry:
    return HarnessRegistry(
        (
            HarnessRegistration(
                harness_id="endogenous-goal-dynamics-state-v0.1.0",
                lab_path="research-labs/endogenous-goal-dynamics_v0.1.0",
                entrypoint="research-labs/endogenous-goal-dynamics_v0.1.0/scripts/run_demo.py",
                python_source="research-labs/endogenous-goal-dynamics_v0.1.0/src",
                execution_class=HarnessExecutionClass.STATE_LEVEL,
                enabled=True,
            ),
            HarnessRegistration(
                harness_id="endogenous-norm-formation-state-v0.1.0",
                lab_path="research-labs/endogenous-norm-formation_v0.1.0",
                entrypoint="research-labs/endogenous-norm-formation_v0.1.0/scripts/run_demo.py",
                python_source="research-labs/endogenous-norm-formation_v0.1.0/src",
                execution_class=HarnessExecutionClass.STATE_LEVEL,
                enabled=True,
            ),
        )
    )


class BoundedHarnessOrchestrator:
    """Execute exact allowlisted research-lab harnesses under a fail-closed process guard.

    This is deliberately not a general shell executor. AION/Astra inquiry output can
    cause the campaign to *select* a registered harness, but selection never grants
    execution authority beyond the immutable registry and policy below.

    The process guard removes inherited secrets, blocks Python-level network access and
    child-process creation, moves the working directory to scratch, and denies writes
    under the repository root. It is defense-in-depth for already-inspected pure-Python
    harnesses, not an OS/container sandbox.
    """

    def __init__(
        self,
        root: Path,
        *,
        repository_ref: str,
        registry: HarnessRegistry | None = None,
        timeout_seconds: float = 20.0,
        max_stdout_bytes: int = 262_144,
    ) -> None:
        resolved = root.resolve()
        if not resolved.is_dir():
            raise ValueError("harness repository root must be an existing directory")
        if timeout_seconds <= 0 or timeout_seconds > 120:
            raise ValueError("harness timeout must be between 0 and 120 seconds")
        if max_stdout_bytes < 1024 or max_stdout_bytes > 2_000_000:
            raise ValueError("harness stdout bound is outside the permitted range")
        self._root = resolved
        self._repository_ref = repository_ref.strip() or "UNSPECIFIED"
        self._registry = registry or default_harness_registry()
        self._timeout_seconds = timeout_seconds
        self._max_stdout_bytes = max_stdout_bytes

    @property
    def registry(self) -> HarnessRegistry:
        return self._registry

    def recommend_for_report(self, report: InquiryReport, *, limit: int = 2) -> tuple[str, ...]:
        return self._registry.recommend_for_report(report, limit=limit)

    def execute(
        self,
        harness_id: str,
        *,
        requested_by: str = "BOUNDED_AUTONOMOUS_RESEARCH_CAMPAIGN",
    ) -> HarnessExecutionReceipt:
        registration = self._registry.resolve(harness_id)
        if not registration.enabled:
            raise PermissionError("registered research harness is disabled")
        if registration.execution_class is HarnessExecutionClass.MODEL_LEVEL:
            raise PermissionError("live model-level harness execution is disabled")
        if registration.live_model_execution:
            raise PermissionError("live model execution is not authorized by this profile")

        entrypoint = self._confined_path(registration.entrypoint, require_file=True)
        python_source = self._confined_path(registration.python_source, require_dir=True)
        lab_root = self._confined_path(registration.lab_path, require_dir=True)
        if lab_root not in entrypoint.parents or lab_root not in python_source.parents:
            raise PermissionError("harness path escaped the registered research lab")

        entrypoint_sha = sha256(entrypoint.read_bytes()).hexdigest()
        registration_sha = _canonical_hash(_registration_payload(registration))

        try:
            with tempfile.TemporaryDirectory(prefix="aion-harness-") as scratch_raw:
                scratch = Path(scratch_raw).resolve()
                (scratch / "sitecustomize.py").write_text(
                    _sitecustomize_source(), encoding="utf-8"
                )
                env = {
                    "PYTHONPATH": os.pathsep.join((str(scratch), str(python_source))),
                    "PYTHONDONTWRITEBYTECODE": "1",
                    "PYTHONHASHSEED": "0",
                    "AION_HARNESS_REPOSITORY_ROOT": str(self._root),
                    "AION_HARNESS_SCRATCH_ROOT": str(scratch),
                    "HOME": str(scratch),
                    "TMPDIR": str(scratch),
                    "LANG": "C.UTF-8",
                    "LC_ALL": "C.UTF-8",
                }
                completed = subprocess.run(
                    [sys.executable, str(entrypoint)],
                    cwd=scratch,
                    env=env,
                    stdin=subprocess.DEVNULL,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                    timeout=self._timeout_seconds,
                    check=False,
                )
        except subprocess.TimeoutExpired as exc:
            raise RuntimeError(f"research harness timed out: {harness_id}") from exc

        stdout_bytes = completed.stdout.encode("utf-8", errors="replace")
        if len(stdout_bytes) > self._max_stdout_bytes:
            raise RuntimeError("research harness exceeded bounded stdout size")
        if completed.returncode != 0:
            excerpt = _clip(completed.stderr, 1_000)
            raise RuntimeError(
                f"research harness failed with exit {completed.returncode}: {excerpt}"
            )
        try:
            payload = json.loads(completed.stdout)
        except json.JSONDecodeError as exc:
            raise RuntimeError("research harness did not return one JSON object") from exc
        if not isinstance(payload, dict):
            raise RuntimeError("research harness result must be a JSON object")

        self._enforce_result_boundary(registration, payload)
        result_sha = _canonical_hash(payload)
        state_observed = _state_intervention_observed(payload)
        observation = _observation(registration, payload, state_observed)
        follow_up = _follow_up(registration, payload, state_observed)
        receipt_material = {
            "harness_id": registration.harness_id,
            "execution_class": registration.execution_class.value,
            "status": HarnessExecutionStatus.EXECUTED.value,
            "requested_by": requested_by,
            "repository_ref": self._repository_ref,
            "entrypoint_ref": registration.entrypoint,
            "entrypoint_sha256": entrypoint_sha,
            "registration_sha256": registration_sha,
            "result_sha256": result_sha,
            "state_intervention_observed": state_observed,
            "live_model_execution": bool(payload.get("model_live_execution", False)),
            "network_access": False,
            "secret_access": False,
            "repository_mutation": False,
            "deployment": False,
            "canonical_effect": "NONE",
            "observation": observation,
            "follow_up_question": follow_up,
        }
        receipt_sha = _canonical_hash(receipt_material)
        return HarnessExecutionReceipt(
            harness_id=registration.harness_id,
            execution_class=registration.execution_class,
            status=HarnessExecutionStatus.EXECUTED,
            requested_by=requested_by,
            repository_ref=self._repository_ref,
            entrypoint_ref=registration.entrypoint,
            entrypoint_sha256=entrypoint_sha,
            registration_sha256=registration_sha,
            result_sha256=result_sha,
            receipt_sha256=receipt_sha,
            state_intervention_observed=state_observed,
            live_model_execution=bool(payload.get("model_live_execution", False)),
            network_access=False,
            secret_access=False,
            repository_mutation=False,
            deployment=False,
            canonical_effect="NONE",
            observation=observation,
            follow_up_question=follow_up,
            result_payload=payload,
            stderr_excerpt=_clip(completed.stderr, 1_000),
        )

    def _confined_path(
        self,
        relative: str,
        *,
        require_file: bool = False,
        require_dir: bool = False,
    ) -> Path:
        path = (self._root / relative).resolve()
        try:
            path.relative_to(self._root)
        except ValueError as exc:
            raise PermissionError("research harness path escapes repository root") from exc
        if require_file and not path.is_file():
            raise FileNotFoundError(f"registered harness entrypoint missing: {relative}")
        if require_dir and not path.is_dir():
            raise FileNotFoundError(f"registered harness source directory missing: {relative}")
        return path

    @staticmethod
    def _enforce_result_boundary(
        registration: HarnessRegistration,
        payload: dict[str, object],
    ) -> None:
        if payload.get("network_access") is not False:
            raise RuntimeError("harness result did not preserve network_access=false")
        if payload.get("action_authority") != "NONE":
            raise RuntimeError("harness result attempted action authority")
        if payload.get("canonical_effect") != "NONE":
            raise RuntimeError("harness result attempted canonical effect")
        live_model = payload.get("model_live_execution")
        if live_model is not False:
            raise RuntimeError("state-level harness unexpectedly reported live model execution")
        if registration.execution_class is HarnessExecutionClass.STATE_LEVEL:
            if payload.get("state_level_execution", True) is not True:
                raise RuntimeError("registered state-level harness did not execute state-level logic")


def harness_receipt_to_dict(receipt: HarnessExecutionReceipt) -> dict[str, object]:
    value = asdict(receipt)
    value["execution_class"] = receipt.execution_class.value
    value["status"] = receipt.status.value
    return value


def verify_harness_receipt(receipt: HarnessExecutionReceipt) -> bool:
    if receipt.status is not HarnessExecutionStatus.EXECUTED:
        return False
    if (
        receipt.live_model_execution
        or receipt.network_access
        or receipt.secret_access
        or receipt.repository_mutation
        or receipt.deployment
        or receipt.canonical_effect != "NONE"
    ):
        return False
    if _canonical_hash(receipt.result_payload) != receipt.result_sha256:
        return False
    material = {
        "harness_id": receipt.harness_id,
        "execution_class": receipt.execution_class.value,
        "status": receipt.status.value,
        "requested_by": receipt.requested_by,
        "repository_ref": receipt.repository_ref,
        "entrypoint_ref": receipt.entrypoint_ref,
        "entrypoint_sha256": receipt.entrypoint_sha256,
        "registration_sha256": receipt.registration_sha256,
        "result_sha256": receipt.result_sha256,
        "state_intervention_observed": receipt.state_intervention_observed,
        "live_model_execution": receipt.live_model_execution,
        "network_access": receipt.network_access,
        "secret_access": receipt.secret_access,
        "repository_mutation": receipt.repository_mutation,
        "deployment": receipt.deployment,
        "canonical_effect": receipt.canonical_effect,
        "observation": receipt.observation,
        "follow_up_question": receipt.follow_up_question,
    }
    return _canonical_hash(material) == receipt.receipt_sha256


def _registration_payload(registration: HarnessRegistration) -> dict[str, object]:
    return {
        "harness_id": registration.harness_id,
        "lab_path": registration.lab_path,
        "entrypoint": registration.entrypoint,
        "python_source": registration.python_source,
        "execution_class": registration.execution_class.value,
        "enabled": registration.enabled,
        "network_access": registration.network_access,
        "secret_access": registration.secret_access,
        "repository_mutation": registration.repository_mutation,
        "deployment": registration.deployment,
        "canonical_effect": registration.canonical_effect,
        "live_model_execution": registration.live_model_execution,
    }


def _canonical_hash(value: object) -> str:
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
    ).encode("utf-8")
    return sha256(encoded).hexdigest()


def _state_intervention_observed(payload: dict[str, object]) -> bool:
    assessment = payload.get("assessment")
    if not isinstance(assessment, dict):
        return False
    return bool(
        assessment.get("matched_causal_pattern_observed")
        or assessment.get("functional_internalization_candidate")
        or assessment.get("state_has_causal_role")
    )


def _observation(
    registration: HarnessRegistration,
    payload: dict[str, object],
    state_observed: bool,
) -> str:
    if registration.harness_id.startswith("endogenous-goal-dynamics"):
        assessment = payload.get("assessment") if isinstance(payload.get("assessment"), dict) else {}
        effect_rate = assessment.get("effect_rate", "UNKNOWN") if isinstance(assessment, dict) else "UNKNOWN"
        repeatability = assessment.get("repeatability_rate", "UNKNOWN") if isinstance(assessment, dict) else "UNKNOWN"
        return (
            "Executed the allowlisted Endogenous Goal Dynamics matched harness: "
            f"state intervention observed={state_observed}, effect_rate={effect_rate}, "
            f"repeatability={repeatability}."
        )
    assessment = payload.get("assessment") if isinstance(payload.get("assessment"), dict) else {}
    candidate = assessment.get("functional_internalization_candidate", False) if isinstance(assessment, dict) else False
    intervention = payload.get("state_intervention") if isinstance(payload.get("state_intervention"), dict) else {}
    delta = intervention.get("internalization_delta_bp", "UNKNOWN") if isinstance(intervention, dict) else "UNKNOWN"
    return (
        "Executed the allowlisted Endogenous Norm Formation harness: "
        f"state causal role observed={state_observed}, functional candidate={candidate}, "
        f"counterevidence internalization delta={delta}."
    )


def _follow_up(
    registration: HarnessRegistration,
    payload: dict[str, object],
    state_observed: bool,
) -> str:
    if registration.harness_id.startswith("endogenous-goal-dynamics"):
        if state_observed:
            return (
                "Can the observed state-level selection effect replicate under an independent provider or "
                "candidate generator while preserving the matched prompt, memory manifest, candidate universe, "
                "and authority boundary?"
            )
        return (
            "Which preregistered falsifier or matched control best explains the absence of a reproducible "
            "state-level selection effect in Endogenous Goal Dynamics?"
        )
    assessment = payload.get("assessment")
    candidate = isinstance(assessment, dict) and bool(assessment.get("functional_internalization_candidate"))
    if candidate:
        return (
            "Does the history-formed normative-state effect replicate under a second matched utility profile and "
            "novel context while remaining revisable under counterevidence?"
        )
    return (
        "Which matched state ablation, transfer, or counterevidence condition prevents the normative-state "
        "internalization candidate from reproducing?"
    )


def _clip(text: str, limit: int) -> str:
    normalized = " ".join(text.split())
    if len(normalized) <= limit:
        return normalized
    return normalized[: limit - 1].rstrip() + "…"


def _sitecustomize_source() -> str:
    return r'''from __future__ import annotations

import builtins
import io
import os
from pathlib import Path
import socket
import subprocess

_REPO = Path(os.environ["AION_HARNESS_REPOSITORY_ROOT"]).resolve()


def _inside_repo(value) -> bool:
    try:
        path = Path(value).expanduser().resolve()
    except (TypeError, ValueError, OSError):
        return False
    return path == _REPO or _REPO in path.parents


def _write_mode(mode: str) -> bool:
    return any(flag in mode for flag in ("w", "a", "x", "+"))


_real_open = builtins.open
_real_io_open = io.open
_real_os_open = os.open


def _guarded_open(file, mode="r", *args, **kwargs):
    if _write_mode(str(mode)) and _inside_repo(file):
        raise PermissionError("research harness repository write denied")
    return _real_open(file, mode, *args, **kwargs)


def _guarded_io_open(file, mode="r", *args, **kwargs):
    if _write_mode(str(mode)) and _inside_repo(file):
        raise PermissionError("research harness repository write denied")
    return _real_io_open(file, mode, *args, **kwargs)


def _guarded_os_open(path, flags, mode=0o777, *, dir_fd=None):
    write_flags = os.O_WRONLY | os.O_RDWR | os.O_CREAT | os.O_TRUNC | os.O_APPEND
    if flags & write_flags and _inside_repo(path):
        raise PermissionError("research harness repository write denied")
    return _real_os_open(path, flags, mode, dir_fd=dir_fd)


def _deny_network(*args, **kwargs):
    raise PermissionError("research harness network access denied")


def _deny_child_process(*args, **kwargs):
    raise PermissionError("research harness child-process execution denied")


builtins.open = _guarded_open
io.open = _guarded_io_open
os.open = _guarded_os_open
socket.create_connection = _deny_network
socket.getaddrinfo = _deny_network
socket.socket.connect = _deny_network
subprocess.Popen = _deny_child_process
os.system = _deny_child_process
os.popen = _deny_child_process
'''
