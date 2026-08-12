import pytest

from embodiment_capability_primitives import (
    ActionCommand,
    CapabilityChannel,
    ChannelKind,
    EmbodimentCapabilityProfile,
    ObservationSample,
)


def channel(channel_id: str = "obs-1", kind: ChannelKind = ChannelKind.OBSERVATION) -> CapabilityChannel:
    return CapabilityChannel(
        channel_id=channel_id,
        kind=kind,
        signal_kind="position",
        enabled=True,
        unit_ref="rad",
        latency_ms=5.0,
        resolution=0.001,
        noise_floor=0.0005,
        evidence_refs=("evidence-1",),
        provenance_refs=("source-1",),
        frame_ref="joint-space",
    )


def profile(*channels: CapabilityChannel) -> EmbodimentCapabilityProfile:
    return EmbodimentCapabilityProfile(
        profile_id="profile-1",
        agent_id="agent-1",
        embodiment_id="embodiment-1",
        template_ref="template-1",
        channels=channels,
        evidence_refs=("profile-evidence",),
        provenance_refs=("profile-source",),
    )


def test_channel_requires_provenance() -> None:
    with pytest.raises(ValueError, match="provenance_refs"):
        CapabilityChannel(
            channel_id="c1",
            kind=ChannelKind.OBSERVATION,
            signal_kind="position",
            enabled=True,
            unit_ref="rad",
            latency_ms=0.0,
            resolution=0.0,
            noise_floor=0.0,
            evidence_refs=("e1",),
            provenance_refs=(),
        )


def test_profile_rejects_duplicate_channel_ids() -> None:
    with pytest.raises(ValueError, match="channel_id"):
        profile(channel("same"), channel("same", ChannelKind.ACTION))


def test_profile_keeps_observation_and_action_distinct() -> None:
    p = profile(channel("obs", ChannelKind.OBSERVATION), channel("act", ChannelKind.ACTION))
    assert [c.channel_id for c in p.enabled_channels(ChannelKind.OBSERVATION)] == ["obs"]
    assert [c.channel_id for c in p.enabled_channels(ChannelKind.ACTION)] == ["act"]


def test_disabled_channel_is_not_enabled_capability() -> None:
    disabled = CapabilityChannel(
        channel_id="off",
        kind=ChannelKind.INTERNAL_OBSERVATION,
        signal_kind="resource_level",
        enabled=False,
        unit_ref="normalized",
        latency_ms=0.0,
        resolution=0.01,
        noise_floor=0.0,
        evidence_refs=("e1",),
        provenance_refs=("p1",),
    )
    assert profile(disabled).enabled_channels() == ()


def test_observation_sample_has_units_source_and_provenance() -> None:
    sample = ObservationSample(
        sample_id="s1",
        subject_ref="agent-1",
        embodiment_id="embodiment-1",
        channel_id="obs-1",
        source_ref="sensor-1",
        value=0.5,
        unit_ref="rad",
        timestamp="2026-08-10T00:00:00Z",
        confidence=0.9,
        evidence_refs=("e1",),
        provenance_refs=("p1",),
        frame_ref="joint-space",
    )
    assert sample.unit_ref == "rad"
    assert sample.source_ref == "sensor-1"


def test_observation_confidence_is_bounded() -> None:
    with pytest.raises(ValueError, match="confidence"):
        ObservationSample(
            sample_id="s1",
            subject_ref="agent-1",
            embodiment_id="embodiment-1",
            channel_id="obs-1",
            source_ref="sensor-1",
            value=0.5,
            unit_ref="rad",
            timestamp="2026-08-10T00:00:00Z",
            confidence=1.2,
            evidence_refs=("e1",),
            provenance_refs=("p1",),
        )


def test_action_command_is_separate_from_observation() -> None:
    cmd = ActionCommand(
        command_id="cmd-1",
        subject_ref="agent-1",
        embodiment_id="embodiment-1",
        channel_id="act-1",
        target_ref="joint-1",
        value=0.2,
        unit_ref="rad",
        issued_at="2026-08-10T00:00:00Z",
        evidence_refs=("e1",),
        provenance_refs=("p1",),
    )
    assert cmd.target_ref == "joint-1"
    assert cmd.volition_claim == "NOT_ESTABLISHED"


def test_nonclaims_are_locked() -> None:
    with pytest.raises(ValueError, match="subjectivity"):
        EmbodimentCapabilityProfile(
            profile_id="p1",
            agent_id="a1",
            embodiment_id="e1",
            template_ref="t1",
            channels=(),
            evidence_refs=("e1",),
            provenance_refs=("p1",),
            subjectivity_claim="ESTABLISHED",
        )


def test_empty_channel_profile_is_valid_control_material() -> None:
    p = profile()
    assert p.enabled_channels() == ()
