"""Execute an explicit validation plan and fail closed on any failed command."""

from __future__ import annotations

from .models import CommandRequest, ValidationPlan, ValidationResult
from .command_runner import CommandRunner


def run_validation(
    validation_id: str,
    plan: ValidationPlan,
    requests: tuple[CommandRequest, ...],
    runner: CommandRunner,
    *,
    occurred_at: str,
) -> ValidationResult:
    results = tuple(runner.run(item, occurred_at=occurred_at) for item in requests)
    return ValidationResult(
        validation_id=validation_id,
        plan=plan,
        command_results=results,
        passed=bool(results) and all(item.status == "PASS" for item in results),
        evidence_paths=tuple(f"audit:{item.result_hash}" for item in results),
    )
