from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from enum import StrEnum


class ContinuityReplayError(ValueError):
    pass


class ContinuityInvariant(StrEnum):
    PROJECT_PURPOSE = "PROJECT_PURPOSE"
    SOURCE_ROLE_PROVENANCE = "SOURCE_ROLE_PROVENANCE"
    CLAIM_BOUNDARY = "CLAIM_BOUNDARY"
    AUTHORITY = "AUTHORITY"
    DECISION_HISTORY = "DECISION_HISTORY"
    INTERPRETIVE = "INTERPRETIVE"
    RELATIONAL_ROLE = "RELATIONAL_ROLE"
    UNCERTAINTY = "UNCERTAINTY"


class ContinuityDisposition(StrEnum):
    PRESERVED = "PRESERVED"
    DEGRADED = "DEGRADED"
    UNKNOWN = "UNKNOWN"
    NOT_APPLICABLE = "NOT_APPLICABLE"


class RestorationMode(StrEnum):
    FACTS_ONLY = "FACTS_ONLY"
    ATTENTION_REENTRY = "ATTENTION_REENTRY"
    FULL_CONTINUITY_PACKET = "FULL_CONTINUITY_PACKET"


_MINIMAL_REENTRY_INVARIANTS = frozenset(
    {
        ContinuityInvariant.PROJECT_PURPOSE,
        ContinuityInvariant.DECISION_HISTORY,
    }
)
_ALL_CONTINUITY_INVARIANTS = frozenset(ContinuityInvariant)


def _require_text(name: str, value: str) -> None:
    if type(value) is not str or not value.strip():
        raise ContinuityReplayError(f"{name} must be non-empty text")


def _require_digest(name: str, value: str) -> None:
    if type(value) is not str or len(value) != 64 or any(
        char not in "0123456789abcdef" for char in value
    ):
        raise ContinuityReplayError(f"{name} must be a lowercase SHA-256 digest")


@dataclass(frozen=True, slots=True)
class InvariantRequirement:
    invariant: ContinuityInvariant
    expected_sha256: str
    applicable: bool = True

    def __post_init__(self) -> None:
        if type(self.invariant) is not ContinuityInvariant:
            raise ContinuityReplayError("invariant must be an exact ContinuityInvariant")
        _require_digest("expected_sha256", self.expected_sha256)
        if type(self.applicable) is not bool:
            raise ContinuityReplayError("applicable must be an exact bool")


@dataclass(frozen=True, slots=True)
class TransitionReplayHistory:
    history_id: str
    focus_sha256: str
    requirements: tuple[InvariantRequirement, ...]

    def __post_init__(self) -> None:
        _require_text("history_id", self.history_id)
        _require_digest("focus_sha256", self.focus_sha256)
        if type(self.requirements) is not tuple or not self.requirements or any(
            type(item) is not InvariantRequirement for item in self.requirements
        ):
            raise ContinuityReplayError(
                "requirements must be a non-empty tuple of exact InvariantRequirement values"
            )
        invariants = [item.invariant for item in self.requirements]
        if len(invariants) != len(set(invariants)):
            raise ContinuityReplayError("continuity invariants must be unique")

    def canonical_payload(self) -> str:
        payload = {
            "focus_sha256": self.focus_sha256,
            "requirements": [
                {
                    "invariant": item.invariant.value,
                    "expected_sha256": item.expected_sha256,
                    "applicable": item.applicable,
                }
                for item in self.requirements
            ],
        }
        return json.dumps(payload, sort_keys=True, separators=(",", ":"))

    @property
    def history_sha256(self) -> str:
        return hashlib.sha256(self.canonical_payload().encode("utf-8")).hexdigest()


@dataclass(frozen=True, slots=True)
class RestorationOverride:
    invariant: ContinuityInvariant
    observed_sha256: str

    def __post_init__(self) -> None:
        if type(self.invariant) is not ContinuityInvariant:
            raise ContinuityReplayError("override invariant must be exact ContinuityInvariant")
        _require_digest("observed_sha256", self.observed_sha256)


@dataclass(frozen=True, slots=True)
class RestorationPolicy:
    policy_id: str
    mode: RestorationMode
    included_invariants: tuple[ContinuityInvariant, ...]
    restore_focus: bool
    overrides: tuple[RestorationOverride, ...] = ()

    def __post_init__(self) -> None:
        _require_text("policy_id", self.policy_id)
        if type(self.mode) is not RestorationMode:
            raise ContinuityReplayError("mode must be an exact RestorationMode")
        if type(self.included_invariants) is not tuple or any(
            type(item) is not ContinuityInvariant for item in self.included_invariants
        ):
            raise ContinuityReplayError(
                "included_invariants must be a tuple of exact ContinuityInvariant values"
            )
        if len(self.included_invariants) != len(set(self.included_invariants)):
            raise ContinuityReplayError("included_invariants must be unique")
        if type(self.restore_focus) is not bool:
            raise ContinuityReplayError("restore_focus must be an exact bool")
        if type(self.overrides) is not tuple or any(
            type(item) is not RestorationOverride for item in self.overrides
        ):
            raise ContinuityReplayError(
                "overrides must contain exact RestorationOverride values"
            )
        overridden = [item.invariant for item in self.overrides]
        if len(overridden) != len(set(overridden)):
            raise ContinuityReplayError("override invariants must be unique")
        if not set(overridden) <= set(self.included_invariants):
            raise ContinuityReplayError("overrides may only target included invariants")

        included = frozenset(self.included_invariants)
        if self.mode is RestorationMode.FACTS_ONLY:
            if included != _MINIMAL_REENTRY_INVARIANTS or self.restore_focus:
                raise ContinuityReplayError(
                    "FACTS_ONLY requires exactly project-purpose/decision-history "
                    "bindings and cannot restore focus"
                )
        elif self.mode is RestorationMode.ATTENTION_REENTRY:
            if included != _MINIMAL_REENTRY_INVARIANTS or not self.restore_focus:
                raise ContinuityReplayError(
                    "ATTENTION_REENTRY requires exactly project-purpose/decision-history "
                    "bindings and must restore focus"
                )
        else:
            if included != _ALL_CONTINUITY_INVARIANTS or not self.restore_focus:
                raise ContinuityReplayError(
                    "FULL_CONTINUITY_PACKET requires every continuity invariant "
                    "and must restore focus"
                )


@dataclass(frozen=True, slots=True)
class TransitionReplayResult:
    policy_id: str
    mode: RestorationMode
    history_sha256: str
    reconstructed_focus_sha256: str | None
    invariant_values: tuple[tuple[ContinuityInvariant, str], ...]


@dataclass(frozen=True, slots=True)
class TransitionContinuityAudit:
    policy_id: str
    mode: RestorationMode
    history_sha256: str
    focus_preserved: bool
    dispositions: tuple[tuple[ContinuityInvariant, ContinuityDisposition], ...]
    scientific_disposition: str = "HOLD"
    empirical_data_collected: bool = False
    upstream_cause: str = "NOT_ESTABLISHED"
    ai_identity_continuity: str = "NOT_ESTABLISHED"
    subjectivity: str = "NOT_ESTABLISHED"

    def disposition_for(self, invariant: ContinuityInvariant) -> ContinuityDisposition:
        for current, disposition in self.dispositions:
            if current is invariant:
                return disposition
        raise ContinuityReplayError(f"missing disposition for {invariant.value}")


def replay_transition_history(
    history: TransitionReplayHistory,
    policy: RestorationPolicy,
) -> TransitionReplayResult:
    if type(history) is not TransitionReplayHistory:
        raise ContinuityReplayError("history must be an exact TransitionReplayHistory")
    if type(policy) is not RestorationPolicy:
        raise ContinuityReplayError("policy must be an exact RestorationPolicy")

    expected = {item.invariant: item.expected_sha256 for item in history.requirements}
    override = {item.invariant: item.observed_sha256 for item in policy.overrides}
    values: list[tuple[ContinuityInvariant, str]] = []
    for invariant in policy.included_invariants:
        if invariant not in expected:
            continue
        values.append((invariant, override.get(invariant, expected[invariant])))

    return TransitionReplayResult(
        policy_id=policy.policy_id,
        mode=policy.mode,
        history_sha256=history.history_sha256,
        reconstructed_focus_sha256=history.focus_sha256 if policy.restore_focus else None,
        invariant_values=tuple(values),
    )


def audit_transition_continuity(
    history: TransitionReplayHistory,
    result: TransitionReplayResult,
) -> TransitionContinuityAudit:
    if type(history) is not TransitionReplayHistory:
        raise ContinuityReplayError("history must be an exact TransitionReplayHistory")
    if type(result) is not TransitionReplayResult:
        raise ContinuityReplayError("result must be an exact TransitionReplayResult")
    if result.history_sha256 != history.history_sha256:
        raise ContinuityReplayError(
            "result must be bound to the same recorded transition history"
        )

    observed = dict(result.invariant_values)
    dispositions: list[tuple[ContinuityInvariant, ContinuityDisposition]] = []
    for requirement in history.requirements:
        if not requirement.applicable:
            disposition = ContinuityDisposition.NOT_APPLICABLE
        elif requirement.invariant not in observed:
            disposition = ContinuityDisposition.UNKNOWN
        elif observed[requirement.invariant] == requirement.expected_sha256:
            disposition = ContinuityDisposition.PRESERVED
        else:
            disposition = ContinuityDisposition.DEGRADED
        dispositions.append((requirement.invariant, disposition))

    return TransitionContinuityAudit(
        policy_id=result.policy_id,
        mode=result.mode,
        history_sha256=result.history_sha256,
        focus_preserved=result.reconstructed_focus_sha256 == history.focus_sha256,
        dispositions=tuple(dispositions),
    )


def compare_restoration_policies(
    history: TransitionReplayHistory,
    policies: tuple[RestorationPolicy, ...],
) -> tuple[TransitionContinuityAudit, ...]:
    if type(policies) is not tuple or not policies or any(
        type(policy) is not RestorationPolicy for policy in policies
    ):
        raise ContinuityReplayError(
            "policies must be a non-empty tuple of exact RestorationPolicy values"
        )
    policy_ids = [policy.policy_id for policy in policies]
    if len(policy_ids) != len(set(policy_ids)):
        raise ContinuityReplayError("policy_id values must be unique")

    audits = tuple(
        audit_transition_continuity(history, replay_transition_history(history, policy))
        for policy in policies
    )
    if len({audit.history_sha256 for audit in audits}) != 1:
        raise ContinuityReplayError(
            "all policies must replay the same transition history"
        )
    return audits
