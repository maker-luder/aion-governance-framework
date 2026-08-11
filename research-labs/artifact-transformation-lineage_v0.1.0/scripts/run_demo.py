from aion_artifact_lineage import ArtifactRef, RunState, TransformationJob, TransformationLedger, TransformationRunEvent, hash_bytes

source = b"public-source-snapshot"
product = b"aion-clean-room-artifact"
job = TransformationJob("external-intake", "clean-room-conversion", "git:fixed-source")
ledger = TransformationLedger()
ledger.append(
    TransformationRunEvent(
        "demo-run",
        job,
        RunState.START,
        "2026-08-11T00:00:00Z",
        materials=(ArtifactRef("source.txt", hash_bytes(source), source_ref="public-repo@commit"),),
        command=("clean-room-convert",),
        environment={"network": "none"},
        source_ref="public-repo@commit",
        approval_ref="human-owner-current-turn",
    )
)
ledger.append(
    TransformationRunEvent(
        "demo-run",
        job,
        RunState.COMPLETE,
        "2026-08-11T00:01:00Z",
        products=(ArtifactRef("aion-module.txt", hash_bytes(product), source_ref="chatgpt-clean-room"),),
        byproducts={"return-value": 0},
        source_ref="public-repo@commit",
        approval_ref="human-owner-current-turn",
    )
)
print({"verified": ledger.verify_products("demo-run", {"aion-module.txt": product}), "canonical_effect": "NONE"})
