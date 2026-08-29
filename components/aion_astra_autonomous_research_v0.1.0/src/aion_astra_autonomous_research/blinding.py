from __future__ import annotations

from dataclasses import dataclass

from aion_triadic_state import canonical_hash


@dataclass(frozen=True, slots=True)
class BlindedInterpretation:
    peer: str
    label: str
    interpretation: str
    evidence_refs: tuple[str, ...]


class BlindedConditionController:
    def __init__(self, experiment_id: str, conditions: tuple[str, ...]) -> None:
        if len(conditions) < 2 or len(set(conditions)) != len(conditions):
            raise ValueError("blinding requires at least two unique conditions")
        self._mapping = {
            f"C-{canonical_hash((experiment_id, condition))[:12].upper()}": condition for condition in conditions
        }
        self._interpretations: dict[tuple[str, str], BlindedInterpretation] = {}
        self._revealed = False

    @property
    def labels(self) -> tuple[str, ...]:
        return tuple(sorted(self._mapping))

    @property
    def mapping_hash(self) -> str:
        return canonical_hash(self._mapping)

    @property
    def revealed(self) -> bool:
        return self._revealed

    def condition_for_controller(self, label: str) -> str:
        return self._mapping[label]

    def record(self, peer: str, label: str, interpretation: str, evidence_refs: tuple[str, ...]) -> None:
        if self._revealed:
            raise ValueError("interpretations cannot be added after condition reveal")
        if peer not in {"AION", "ASTRA"} or label not in self._mapping or not interpretation.strip():
            raise ValueError("invalid blinded interpretation")
        key = (peer, label)
        if key in self._interpretations:
            raise ValueError("duplicate blinded interpretation")
        self._interpretations[key] = BlindedInterpretation(peer, label, interpretation, evidence_refs)

    def reveal(self) -> dict[str, str]:
        required = {(peer, label) for peer in ("AION", "ASTRA") for label in self.labels}
        if set(self._interpretations) != required:
            raise ValueError("mapping remains blinded until both independent peers interpret every condition")
        self._revealed = True
        return dict(sorted(self._mapping.items()))

    @property
    def interpretations(self) -> tuple[BlindedInterpretation, ...]:
        return tuple(self._interpretations[key] for key in sorted(self._interpretations))
