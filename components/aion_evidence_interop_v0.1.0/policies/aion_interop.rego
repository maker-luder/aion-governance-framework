package aion.interop

default allow := false

deny contains "SOURCE_VALIDATION_NOT_PASS" if {
  input.source.validation_status != "PASS"
}

deny contains "CANONICAL_EFFECT_OPEN" if {
  input.boundaries.canonical_effect != "NONE"
}

deny contains "DEPLOYMENT_TRUE" if {
  input.boundaries.deployment != false
}

deny contains "RESEARCH_EXECUTION_REQUESTED" if {
  input.boundaries.research_execution != false
}

deny contains "MODEL_EXECUTION_REQUESTED" if {
  input.boundaries.model_execution != false
}

deny contains "NETWORK_ACCESS_REQUESTED" if {
  input.boundaries.network_access != false
}

deny contains "SUBJECTIVITY_PROMOTION_DETECTED" if {
  input.boundaries.subjectivity_conclusion != "NOT_ESTABLISHED"
}

deny contains "IDENTITY_PROMOTION_DETECTED" if {
  input.boundaries.identity_continuity_conclusion != "NOT_ESTABLISHED"
}

deny contains "IVV_PROMOTION_DETECTED" if {
  input.boundaries.independent_ivv != "NOT_ACHIEVED"
}

required_artifacts := {
  "prov.jsonld",
  "ro-crate/ro-crate-metadata.json",
  "inspect/task-manifest.json",
  "inspect/dataset.jsonl",
}

deny contains "MISSING_DERIVATION_HASH" if {
  some name in required_artifacts
  not input.artifact_digests[name]
}

allow if {
  count(deny) == 0
}
