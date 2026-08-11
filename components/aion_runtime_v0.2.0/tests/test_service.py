import pytest

from aion_runtime_v2.service import RuntimeServiceEnvelope, ServiceState


def test_service_lifecycle_and_drain():
    service = RuntimeServiceEnvelope(max_concurrency=1)
    service.start()
    assert service.state is ServiceState.READY
    service.begin_request()
    assert service.state is ServiceState.RUNNING
    service.drain()
    assert service.state is ServiceState.DRAINING
    service.end_request()
    assert service.state is ServiceState.STOPPED


def test_backpressure_degrades():
    service = RuntimeServiceEnvelope(max_concurrency=1)
    service.start()
    service.begin_request()
    with pytest.raises(RuntimeError):
        service.begin_request()
    assert service.state is ServiceState.DEGRADED
