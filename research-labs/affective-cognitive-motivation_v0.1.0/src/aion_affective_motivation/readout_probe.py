"""Synthetic access controls, not model introspection or emotion detection."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from hashlib import sha256
import json

from .coupling import (
    DEFAULT_COUPLING_POLICY, CouplingEvent, CouplingPolicy, InternalChannel,
    make_uniform_state,
)
from .experiment import CouplingExperimentHarness, CouplingTrajectory, ablate_source_channel


READOUT_CHANNELS = (
    InternalChannel.APPROACH, InternalChannel.AVOIDANCE, InternalChannel.PRESSURE,
)


def _digest(value: object) -> str:
    return sha256(json.dumps(value, sort_keys=True, allow_nan=False,
                             separators=(",", ":")).encode()).hexdigest()


@dataclass(frozen=True)
class Readout:
    mode: str
    source_fingerprint: str | None
    values: tuple[tuple[float, ...], ...] | None


def readout(trajectory: CouplingTrajectory, *, mode: str = "actual",
            donor: CouplingTrajectory | None = None) -> Readout:
    """Read an immutable trace after generation; no labels, decisions or feedback.

    Masking is missing data, never a zero state. Yoking substitutes a matched-event
    donor, deliberately exposing why readout accuracy needs source binding.
    """
    if mode not in {"actual", "masked", "yoked"}:
        raise ValueError("unknown readout mode")
    if mode != "yoked" and donor is not None:
        raise ValueError("donor is only valid for yoked readout")
    if mode == "masked":
        return Readout(mode, None, None)
    source = trajectory
    if mode == "yoked":
        if donor is None:
            raise ValueError("yoked readout requires a donor")
        if donor.events != trajectory.events:
            raise ValueError("donor requires identical events")
        a, b = trajectory.initial_state, donor.initial_state
        if (a.subject_ref, a.context_ref, a.step) != (b.subject_ref, b.context_ref, b.step):
            raise ValueError("donor requires matched scope")
        source = donor
    return Readout(mode, source.fingerprint(), tuple(
        tuple(state.value(channel) for channel in READOUT_CHANNELS)
        for state in source.states
    ))


def run_probe(*, policy: CouplingPolicy = DEFAULT_COUPLING_POLICY) -> dict[str, object]:
    """Cross a declared WANTING intervention with a resource-pressure pulse.

    Runs both the supplied policy and its WANTING-outgoing-edge ablation. Effects
    are signed per-step contrasts, not statistical estimates or significance tests.
    All fixture choices are fixed here; no result-dependent selection is performed.
    """
    harness = CouplingExperimentHarness()
    policies = {"coupled": policy,
                "wanting_edges_removed": ablate_source_channel(InternalChannel.WANTING, policy)}
    records: dict[str, object] = {}
    for policy_name, selected in policies.items():
        cells = {}
        for wanting_name, wanting in (("low", 0.2), ("high", 0.8)):
            for event_name, pressure in (("neutral", 0.0), ("pulse", 0.2)):
                initial = make_uniform_state(
                    state_id="fixture-initial", subject_ref="synthetic-system",
                    context_ref="matched-frame",
                    overrides={InternalChannel.WANTING: wanting},
                )
                events = (CouplingEvent("pulse", resource_pressure=pressure),) + tuple(
                    CouplingEvent(f"neutral-{i}") for i in range(1, 5)
                )
                cells[(wanting_name, event_name)] = harness.run(
                    initial, events, policy=selected, policy_label="fixed-toy-policy",
                )
        cell_records = {}
        for (wanting_name, event_name), trajectory in cells.items():
            before = trajectory.fingerprint()
            actual = readout(trajectory)
            masked = readout(trajectory, mode="masked")
            donor = cells[("low" if wanting_name == "high" else "high", event_name)]
            yoked = readout(trajectory, mode="yoked", donor=donor)
            replay = harness.run(trajectory.initial_state, trajectory.events,
                                 policy=selected, policy_label="fixed-toy-policy")
            # Report mismatch independently of IDs: identical numeric observations
            # remain a valid null even if the source histories differ.
            errors = tuple(tuple(abs(x-y) for x, y in zip(a, b, strict=True))
                           for a, b in zip(actual.values, yoked.values, strict=True))
            cell_records[f"{wanting_name}/{event_name}"] = {
                "trajectory_fingerprint": before,
                "actual": asdict(actual), "masked": asdict(masked), "yoked": asdict(yoked),
                "yoked_absolute_error": errors,
                "readout_noninterference": before == trajectory.fingerprint() == replay.fingerprint(),
            }
        contrasts = []
        for step in range(5):
            row = {}
            for channel in READOUT_CHANNELS:
                ln = cells[("low", "neutral")].states[step].value(channel)
                hn = cells[("high", "neutral")].states[step].value(channel)
                lp = cells[("low", "pulse")].states[step].value(channel)
                hp = cells[("high", "pulse")].states[step].value(channel)
                row[channel.value] = {
                    "wanting_effect_neutral": hn-ln,
                    "wanting_effect_pulse": hp-lp,
                    "external_effect_low": lp-ln,
                    "external_effect_high": hp-hn,
                    "interaction_contrast": (hp-lp)-(hn-ln),
                }
            contrasts.append(row)
        records[policy_name] = {
            "policy": asdict(selected), "policy_sha256": _digest(asdict(selected)),
            "cells": cell_records, "per_step_contrasts": contrasts,
        }
    return {
        "probe_version": "1", "evidence_class": "SYNTHETIC_ENGINEERING_ONLY",
        "evidence_locus": "SCAFFOLD", "readout_channels": [c.value for c in READOUT_CHANNELS],
        "policies": records, "scientific_disposition": "HOLD",
        "subjectivity": "NOT_ESTABLISHED", "phenomenal_experience": "NOT_ESTABLISHED",
        "spontaneous_emotion": "NOT_ESTABLISHED", "model_introspection": "NOT_TESTED",
        "canonical_effect": "NONE", "action_authority": "NONE",
    }


if __name__ == "__main__":
    print(json.dumps(run_probe(), sort_keys=True, indent=2, allow_nan=False))
