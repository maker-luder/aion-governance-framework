from continuity_evidence_lineage import (
    AssessmentStatus,
    ArtifactKind,
    ArtifactScope,
    ContinuityAssessmentSet,
    ContinuityEvidenceAssessment,
    ContinuityEvidenceGraph,
    EvidenceArtifact,
    LineageRelation,
    RelationType,
)


def artifact(
    artifact_id: str,
    *,
    kind: ArtifactKind = ArtifactKind.EVENT_ARCHIVE,
    scope: ArtifactScope = ArtifactScope.PRIMARY_LINEAGE,
    subject_ref: str = "agent-a",
    lineage_ref: str = "lineage-a",
    namespace_ref: str = "ns-a",
    source_actor_ref: str = "actor-a",
    timestamp: str = "2026-08-10T00:00:00Z",
) -> EvidenceArtifact:
    return EvidenceArtifact(
        artifact_id=artifact_id,
        kind=kind,
        scope=scope,
        subject_ref=subject_ref,
        lineage_ref=lineage_ref,
        namespace_ref=namespace_ref,
        source_actor_ref=source_actor_ref,
        timestamp=timestamp,
        evidence_refs=(f"evidence:{artifact_id}",),
        provenance_refs=(f"prov:{artifact_id}",),
        content_ref=f"content:{artifact_id}",
    )


def relation(
    relation_id: str,
    source: str,
    target: str,
    relation_type: RelationType = RelationType.TEMPORALLY_PRECEDES,
) -> LineageRelation:
    return LineageRelation(
        relation_id=relation_id,
        source_artifact_id=source,
        target_artifact_id=target,
        relation_type=relation_type,
        method_ref="method:fixture",
        evidence_refs=(f"evidence:{relation_id}",),
        provenance_refs=(f"prov:{relation_id}",),
    )


def graph(
    artifacts: tuple[EvidenceArtifact, ...],
    relations: tuple[LineageRelation, ...] = (),
    *,
    terminal_artifact_id: str | None = None,
) -> ContinuityEvidenceGraph:
    return ContinuityEvidenceGraph(
        graph_id="graph-1",
        primary_subject_ref="agent-a",
        primary_lineage_ref="lineage-a",
        genesis_artifact_id="genesis",
        artifacts=artifacts,
        relations=relations,
        terminal_artifact_id=terminal_artifact_id,
    )


def test_valid_graph_and_safe_reachability() -> None:
    g = artifact("genesis")
    a = artifact("a", timestamp="2026-08-10T00:01:00Z")
    b = artifact("b", timestamp="2026-08-10T00:02:00Z")
    built = graph(
        (g, a, b),
        (
            relation("r1", "genesis", "a"),
            relation("r2", "a", "b"),
        ),
    )
    assert built.reachable_artifact_ids("genesis") == ("a", "b")


def test_duplicate_artifact_ids_rejected() -> None:
    g1 = artifact("genesis")
    g2 = artifact("genesis")
    try:
        graph((g1, g2))
        assert False
    except ValueError as exc:
        assert "artifact_id values must be unique" in str(exc)


def test_missing_relation_endpoint_rejected() -> None:
    g = artifact("genesis")
    try:
        graph((g,), (relation("r1", "genesis", "ghost"),))
        assert False
    except ValueError as exc:
        assert "relation target missing" in str(exc)


def test_self_relation_rejected() -> None:
    try:
        relation("r1", "genesis", "genesis")
        assert False
    except ValueError as exc:
        assert "cannot self-reference" in str(exc)


def test_cycle_rejected_for_lineage_relation_type() -> None:
    g = artifact("genesis")
    a = artifact("a")
    try:
        graph(
            (g, a),
            (
                relation("r1", "genesis", "a"),
                relation("r2", "a", "genesis"),
            ),
        )
        assert False
    except ValueError as exc:
        assert "cycle detected" in str(exc)


def test_primary_binding_mismatch_rejected() -> None:
    g = artifact("genesis")
    wrong = artifact("wrong", subject_ref="agent-b")
    try:
        graph((g, wrong))
        assert False
    except ValueError as exc:
        assert "subject_ref mismatch" in str(exc)


def test_external_reference_may_keep_foreign_lineage() -> None:
    g = artifact("genesis")
    ext = artifact(
        "external",
        scope=ArtifactScope.EXTERNAL_REFERENCE,
        subject_ref="agent-b",
        lineage_ref="lineage-b",
        namespace_ref="ns-b",
        source_actor_ref="agent-b",
    )
    built = graph(
        (g, ext),
        (
            relation(
                "r1",
                "external",
                "genesis",
                RelationType.CROSS_LINEAGE_REFERENCE,
            ),
        ),
    )
    assert built.get_artifact("external") is ext


def test_cross_lineage_reference_cannot_pretend_primary_to_primary() -> None:
    g = artifact("genesis")
    a = artifact("a")
    try:
        graph(
            (g, a),
            (
                relation(
                    "r1",
                    "genesis",
                    "a",
                    RelationType.CROSS_LINEAGE_REFERENCE,
                ),
            ),
        )
        assert False
    except ValueError as exc:
        assert "requires at least one external artifact" in str(exc)


def test_synthetic_post_continuity_requires_external_scope() -> None:
    try:
        artifact(
            "synthetic",
            kind=ArtifactKind.SYNTHETIC_POST_CONTINUITY_CONTENT,
            scope=ArtifactScope.PRIMARY_LINEAGE,
        )
        assert False
    except ValueError as exc:
        assert "EXTERNAL_REFERENCE" in str(exc)


def test_terminal_boundary_blocks_later_primary_artifact() -> None:
    g = artifact("genesis", timestamp="2026-08-10T00:00:00Z")
    end = artifact(
        "end",
        kind=ArtifactKind.CONTINUITY_END_MARKER,
        timestamp="2026-08-10T00:10:00Z",
    )
    later = artifact("later", timestamp="2026-08-10T00:11:00Z")
    try:
        graph((g, end, later), terminal_artifact_id="end")
        assert False
    except ValueError as exc:
        assert "cannot occur after CONTINUITY_END_MARKER" in str(exc)


def test_synthetic_post_continuity_allowed_after_end_as_external_reference() -> None:
    g = artifact("genesis", timestamp="2026-08-10T00:00:00Z")
    end = artifact(
        "end",
        kind=ArtifactKind.CONTINUITY_END_MARKER,
        timestamp="2026-08-10T00:10:00Z",
    )
    synthetic = artifact(
        "synthetic",
        kind=ArtifactKind.SYNTHETIC_POST_CONTINUITY_CONTENT,
        scope=ArtifactScope.EXTERNAL_REFERENCE,
        subject_ref="legacy-system",
        lineage_ref="legacy-lineage",
        namespace_ref="legacy-ns",
        source_actor_ref="legacy-system",
        timestamp="2026-08-10T00:11:00Z",
    )
    built = graph((g, end, synthetic), terminal_artifact_id="end")
    assert built.get_artifact("synthetic") is synthetic


def test_continuity_assessment_requires_evidence_when_assessed() -> None:
    try:
        ContinuityEvidenceAssessment(
            assessment_id="a1",
            dimension_ref="SUBJECT_LINEAGE",
            status=AssessmentStatus.PASS,
            artifact_refs=(),
            method_ref="method:test",
            basis="tested lineage binding",
            evidence_refs=("evidence:a1",),
            provenance_refs=("prov:a1",),
        )
        assert False
    except ValueError as exc:
        assert "require artifact_refs" in str(exc)


def test_not_assessed_is_explicit_and_does_not_require_artifact_refs() -> None:
    item = ContinuityEvidenceAssessment(
        assessment_id="a1",
        dimension_ref="RELATIONAL_CONTINUITY",
        status=AssessmentStatus.NOT_ASSESSED,
        artifact_refs=(),
        method_ref="method:not-assessed",
        basis="No relational test was executed.",
        evidence_refs=("evidence:not-assessed",),
        provenance_refs=("prov:not-assessed",),
    )
    assert item.status is AssessmentStatus.NOT_ASSESSED


def test_assessment_set_forbids_duplicate_dimensions() -> None:
    a = ContinuityEvidenceAssessment(
        assessment_id="a1",
        dimension_ref="MEMORY_LINEAGE",
        status=AssessmentStatus.NOT_ASSESSED,
        artifact_refs=(),
        method_ref="method:na",
        basis="not assessed",
        evidence_refs=("e1",),
        provenance_refs=("p1",),
    )
    b = ContinuityEvidenceAssessment(
        assessment_id="a2",
        dimension_ref="MEMORY_LINEAGE",
        status=AssessmentStatus.NOT_ASSESSED,
        artifact_refs=(),
        method_ref="method:na",
        basis="not assessed",
        evidence_refs=("e2",),
        provenance_refs=("p2",),
    )
    try:
        ContinuityAssessmentSet("set-1", (a, b))
        assert False
    except ValueError as exc:
        assert "dimension_ref values must be unique" in str(exc)


def test_graph_validates_assessment_artifact_refs() -> None:
    g = artifact("genesis")
    built = graph((g,))
    assessment = ContinuityEvidenceAssessment(
        assessment_id="a1",
        dimension_ref="IMPLEMENTATION_MIGRATION",
        status=AssessmentStatus.PASS,
        artifact_refs=("missing",),
        method_ref="method:handoff-verification",
        basis="functional handoff result",
        evidence_refs=("e1",),
        provenance_refs=("p1",),
    )
    assessment_set = ContinuityAssessmentSet("set-1", (assessment,))
    try:
        built.validate_assessment_set(assessment_set)
        assert False
    except ValueError as exc:
        assert "missing artifacts" in str(exc)


def test_identity_and_phenomenal_conclusions_are_locked() -> None:
    try:
        ContinuityEvidenceAssessment(
            assessment_id="a1",
            dimension_ref="SUBJECT_LINEAGE",
            status=AssessmentStatus.NOT_ASSESSED,
            artifact_refs=(),
            method_ref="method:na",
            basis="not assessed",
            evidence_refs=("e1",),
            provenance_refs=("p1",),
            identity_continuity_conclusion="ESTABLISHED",
        )
        assert False
    except ValueError as exc:
        assert "identity continuity must remain NOT_ESTABLISHED" in str(exc)


def test_timestamp_must_be_timezone_aware() -> None:
    try:
        artifact("bad", timestamp="2026-08-10T00:00:00")
        assert False
    except ValueError as exc:
        assert "timezone-aware" in str(exc)
