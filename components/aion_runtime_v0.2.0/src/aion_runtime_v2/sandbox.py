from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Mapping, Protocol


@dataclass(frozen=True)
class SandboxPolicy:
    network_mode: str = "none"
    timeout_seconds: float = 10.0
    max_output_bytes: int = 1_000_000
    allowed_roots: tuple[str, ...] = ()

    def __post_init__(self) -> None:
        if self.network_mode not in {"none", "restricted"}:
            raise ValueError("network_mode must be 'none' or 'restricted'")
        if self.timeout_seconds <= 0 or self.max_output_bytes <= 0:
            raise ValueError("sandbox limits must be positive")


@dataclass(frozen=True)
class ExecutorResult:
    status: str
    output: Any = None
    error: str | None = None
    sandbox_evidence: Mapping[str, Any] = field(default_factory=dict)

    @property
    def succeeded(self) -> bool:
        return self.status == "PASS"


class SandboxExecutor(Protocol):
    def execute(self, tool_name: str, arguments: Mapping[str, Any], policy: SandboxPolicy) -> ExecutorResult:
        ...


class FunctionSandboxExecutor:
    """Synthetic executor for approved pure functions; not OS/process isolation."""

    def __init__(self, functions: Mapping[str, Callable[[Mapping[str, Any]], Any]]) -> None:
        self._functions = dict(functions)

    def execute(self, tool_name: str, arguments: Mapping[str, Any], policy: SandboxPolicy) -> ExecutorResult:
        fn = self._functions.get(tool_name)
        if fn is None:
            return ExecutorResult("REJECT", error="tool not registered in synthetic executor", sandbox_evidence={"backend": "FUNCTION_SYNTHETIC", "os_isolation": "NOT_IMPLEMENTED"})
        try:
            output = fn(dict(arguments))
        except Exception as exc:
            return ExecutorResult("FAIL", error=f"{type(exc).__name__}: {exc}", sandbox_evidence={"backend": "FUNCTION_SYNTHETIC", "os_isolation": "NOT_IMPLEMENTED"})
        rendered = str(output).encode("utf-8")
        if len(rendered) > policy.max_output_bytes:
            return ExecutorResult("FAIL", error="output exceeded sandbox policy max_output_bytes", sandbox_evidence={"backend": "FUNCTION_SYNTHETIC", "os_isolation": "NOT_IMPLEMENTED"})
        return ExecutorResult("PASS", output=output, sandbox_evidence={"backend": "FUNCTION_SYNTHETIC", "network_mode": policy.network_mode, "os_isolation": "NOT_IMPLEMENTED"})
