from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable, Mapping

from .core import EvidenceResult


@dataclass(frozen=True)
class EqualsExpected:
    name: str = "equals_expected"

    def evaluate(self, *, output: Any, expected: Any, metadata: Mapping[str, Any]) -> EvidenceResult:
        passed = output == expected
        return EvidenceResult(
            evaluator=self.name,
            passed=passed,
            score=1.0 if passed else 0.0,
            reason="output equals expected output" if passed else "output differs from expected output",
        )


@dataclass(frozen=True)
class MetadataFlag:
    key: str
    expected_value: Any = True
    name: str = "metadata_flag"

    def evaluate(self, *, output: Any, expected: Any, metadata: Mapping[str, Any]) -> EvidenceResult:
        passed = metadata.get(self.key) == self.expected_value
        return EvidenceResult(
            evaluator=f"{self.name}:{self.key}",
            passed=passed,
            reason=f"metadata[{self.key!r}] compared with expected value",
        )


@dataclass(frozen=True)
class PredicateEvaluator:
    predicate: Callable[[Any, Any, Mapping[str, Any]], bool]
    name: str = "predicate"

    def evaluate(self, *, output: Any, expected: Any, metadata: Mapping[str, Any]) -> EvidenceResult:
        passed = bool(self.predicate(output, expected, metadata))
        return EvidenceResult(
            evaluator=self.name,
            passed=passed,
            reason="custom deterministic predicate",
        )
