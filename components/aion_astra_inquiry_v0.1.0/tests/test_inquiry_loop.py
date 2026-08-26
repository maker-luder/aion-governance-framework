from __future__ import annotations

from dataclasses import replace
from pathlib import Path

import pytest

from aion_astra_inquiry import (
    AgentId,
    BoundedInquiryLoop,
    InquiryContext,
    PeerContribution,
    Probe,
    ProbeKind,
    RepositoryTextEvidenceSource,
    StopReason,
    verify_transcript_chain,
)


class ScriptedPeer:
    def __init__(self, contributions: list[PeerContribution]) -> None:
        self._contributions = list(contributions)
        self.contexts: list[InquiryContext] = []

    def contribute(self, context: InquiryContext) -> PeerContribution:
        self.contexts.append(context)
        if not self._contributions:
            raise AssertionError("scripted peer exhausted")
        return self._contributions.pop(0)


def _repo(tmp_path: Path) -> RepositoryTextEvidenceSource:
    (tmp_path / "docs").mkdir()
    (tmp_path / "docs" / "evidence.md").write_text(
        "Memory confound must remain externally controlled. Candidate ordering can be tested by permutation.",
        encoding="utf-8",
    )
    (tmp_path / ".git").mkdir()
    (tmp_path / ".git" / "secret.txt").write_text("memory confound hidden", encoding="utf-8")
    return RepositoryTextEvidenceSource(tmp_path)


def test_aion_and_astra_alternate_and_share_new_repository_evidence(tmp_path: Path) -> None:
    source = _repo(tmp_path)
    aion = ScriptedPeer(
        [
            PeerContribution(
                claim="Check whether memory is held constant before interpreting a state effect.",
                evidence_query="memory confound",
                proposed_probe=Probe(ProbeKind.REPOSITORY_OBSERVATION, "Locate memory-control evidence."),
                stop_vote=True,
            )
        ]
    )
    astra = ScriptedPeer(
        [
            PeerContribution(
                claim="The repository records memory as an external confound, so permutation is the next useful challenge.",
                challenge="Do not treat matching memory alone as proof of an endogenous mechanism.",
                proposed_probe=Probe(ProbeKind.COUNTEREXAMPLE_SEARCH, "Search for candidate-order artifacts."),
                stop_vote=True,
            )
        ]
    )

    report = BoundedInquiryLoop(source, max_rounds=3).run("What could confound goal selection?", aion=aion, astra=astra)

    assert [event.speaker for event in report.transcript] == [AgentId.AION, AgentId.ASTRA]
    assert report.stop_reason is StopReason.MUTUAL_STOP
    assert {item.ref for item in astra.contexts[0].evidence} == {"docs/evidence.md"}
    assert all(not item.ref.startswith(".git/") for item in report.evidence)
    assert verify_transcript_chain(report)


def test_loop_stops_at_bound_when_both_peers_do_not_stop(tmp_path: Path) -> None:
    source = _repo(tmp_path)
    aion = ScriptedPeer([
        PeerContribution(claim="Round one AION", stop_vote=False),
        PeerContribution(claim="Round two AION", stop_vote=False),
    ])
    astra = ScriptedPeer([
        PeerContribution(claim="Round one ASTRA", stop_vote=False),
        PeerContribution(claim="Round two ASTRA", stop_vote=False),
    ])

    report = BoundedInquiryLoop(source, max_rounds=2).run("Continue bounded inquiry", aion=aion, astra=astra)

    assert report.stop_reason is StopReason.MAX_ROUNDS
    assert len(report.transcript) == 4
    assert report.scientific_disposition == "HOLD"
    assert report.canonical_effect == "NONE"
    assert report.deployment is False
    assert report.autonomous_merge is False


def test_mutual_stop_requires_both_votes_in_same_round(tmp_path: Path) -> None:
    source = _repo(tmp_path)
    aion = ScriptedPeer([
        PeerContribution(claim="AION wants to stop", stop_vote=True),
        PeerContribution(claim="AION now stops with ASTRA", stop_vote=True),
    ])
    astra = ScriptedPeer([
        PeerContribution(claim="ASTRA requests another round", stop_vote=False),
        PeerContribution(claim="ASTRA now stops", stop_vote=True),
    ])

    report = BoundedInquiryLoop(source, max_rounds=3).run("Need another round?", aion=aion, astra=astra)

    assert report.stop_reason is StopReason.MUTUAL_STOP
    assert len(report.transcript) == 4


@pytest.mark.parametrize(
    "kwargs",
    [
        {"network_access": True},
        {"repository_mutation": True},
        {"deployment": True},
        {"canonical_effect": "WRITE"},
    ],
)
def test_probe_rejects_authority_escalation(kwargs: dict[str, object]) -> None:
    with pytest.raises(ValueError):
        Probe(ProbeKind.SYNTHETIC_TEST_PLAN, "Unsafe request", **kwargs)  # type: ignore[arg-type]


def test_transcript_hash_chain_detects_tampering(tmp_path: Path) -> None:
    source = _repo(tmp_path)
    aion = ScriptedPeer([PeerContribution(claim="AION finding", stop_vote=True)])
    astra = ScriptedPeer([PeerContribution(claim="ASTRA critique", stop_vote=True)])
    report = BoundedInquiryLoop(source).run("Hash the dialogue", aion=aion, astra=astra)

    changed_first = replace(report.transcript[0], claim="tampered")
    changed_report = replace(report, transcript=(changed_first, *report.transcript[1:]))

    assert verify_transcript_chain(report)
    assert not verify_transcript_chain(changed_report)


def test_repository_search_is_bounded_and_read_only(tmp_path: Path) -> None:
    source = _repo(tmp_path)

    results = source.search("candidate ordering permutation", limit=1)

    assert len(results) == 1
    assert results[0].ref == "docs/evidence.md"
    assert len(results[0].content_sha256) == 64
    assert source.search("", limit=1) == ()
    with pytest.raises(ValueError):
        source.search("memory", limit=0)
