from __future__ import annotations

from dataclasses import dataclass
from enum import Enum


class ServiceState(str, Enum):
    STARTING = "STARTING"
    READY = "READY"
    RUNNING = "RUNNING"
    DEGRADED = "DEGRADED"
    DRAINING = "DRAINING"
    STOPPED = "STOPPED"
    FAILED = "FAILED"


@dataclass
class RuntimeServiceEnvelope:
    max_concurrency: int = 1
    state: ServiceState = ServiceState.STOPPED
    in_flight: int = 0

    def __post_init__(self) -> None:
        if self.max_concurrency <= 0:
            raise ValueError("max_concurrency must be positive")

    def start(self) -> None:
        if self.state not in {ServiceState.STOPPED, ServiceState.FAILED}:
            raise RuntimeError(f"cannot start from {self.state.value}")
        self.state = ServiceState.STARTING
        self.state = ServiceState.READY

    def begin_request(self) -> None:
        if self.state not in {ServiceState.READY, ServiceState.RUNNING}:
            raise RuntimeError(f"service not accepting work in {self.state.value}")
        if self.in_flight >= self.max_concurrency:
            self.state = ServiceState.DEGRADED
            raise RuntimeError("backpressure: max_concurrency reached")
        self.in_flight += 1
        self.state = ServiceState.RUNNING

    def end_request(self) -> None:
        if self.in_flight <= 0:
            raise RuntimeError("no in-flight request to end")
        self.in_flight -= 1
        if self.state is ServiceState.DRAINING:
            if self.in_flight == 0:
                self.state = ServiceState.STOPPED
        elif self.in_flight == 0:
            self.state = ServiceState.READY

    def drain(self) -> None:
        if self.state not in {ServiceState.READY, ServiceState.RUNNING, ServiceState.DEGRADED}:
            raise RuntimeError(f"cannot drain from {self.state.value}")
        self.state = ServiceState.DRAINING
        if self.in_flight == 0:
            self.state = ServiceState.STOPPED

    def fail(self) -> None:
        self.state = ServiceState.FAILED

    def health(self) -> dict[str, object]:
        return {"state": self.state.value, "ready": self.state in {ServiceState.READY, ServiceState.RUNNING}, "accepting_requests": self.state in {ServiceState.READY, ServiceState.RUNNING}, "in_flight": self.in_flight, "max_concurrency": self.max_concurrency, "canonical_effect": "NONE"}
