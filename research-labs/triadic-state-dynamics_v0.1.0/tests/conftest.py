from __future__ import annotations

from aion_triadic_state import ConflictStatus, MotivationalStateView, NormativeConstraint, NormativeState, SelfWorldModel, TriadicStateSnapshot


def make_snapshot(step: int = 0) -> TriadicStateSnapshot:
    motivation = MotivationalStateView(f"mot-{step}", "AION", "ctx", "aion_affective_motivation.MotivationalState", f"signal-{step}", ("ev:mot",))
    self_world = SelfWorldModel(f"sw-{step}", "AION", "ctx", ("repository observation",), ("no action authority",), ("synthetic fixture",), 0.2, 0.8, evidence_refs=("ev:self",))
    normative = NormativeState(f"norm-{step}", "AION", "ctx", (NormativeConstraint("NO_WRITE", "policy:test", "repository", 100, True, ConflictStatus.NONE, 0.0, ("ev:norm",)),), ("prov:norm",))
    return TriadicStateSnapshot(f"triadic-{step}", "AION", "ctx", step, None if step == 0 else f"prior-{step}", motivation, self_world, normative, ("ev:base",), ("prov:base",))
