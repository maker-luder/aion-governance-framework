package aion.interop

default allow := false

deny contains "SOURCE_VALIDATION_NOT_PASS" if {
  object.get(object.get(input, "source", {}), "validation_status", null) != "PASS"
}

deny contains "CANONICAL_EFFECT_OPEN" if {
  object.get(object.get(input, "boundaries", {}), "canonical_effect", null) != "NONE"
}

deny contains "DEPLOYMENT_TRUE" if {
  object.get(object.get(input, "boundaries", {}), "deployment", null) != false
}

deny contains "RESEARCH_EXECUTION_REQUESTED" if {
  object.get(object.get(input, "boundaries", {}), "research_execution", null) != false
}

deny contains "MODEL_EXECUTION_REQUESTED" if {
  object.get(object.get(input, "boundaries", {}), "model_execution", null) != false
}

deny contains "NETWORK_ACCESS_REQUESTED" if {
  object.get(object.get(input, "boundaries", {}), "network_access", null) != false
}

deny contains "SUBJECTIVITY_PROMOTION_DETECTED" if {
  object.get(object.get(input, "boundaries", {}), "subjectivity_conclusion", null) != "NOT_ESTABLISHED"
}

deny contains "IDENTITY_PROMOTION_DETECTED" if {
  object.get(object.get(input, "boundaries", {}), "identity_continuity_conclusion", null) != "NOT_ESTABLISHED"
}

deny contains "IVV_PROMOTION_DETECTED" if {
  object.get(object.get(input, "boundaries", {}), "independent_ivv", null) != "NOT_ACHIEVED"
}

deny contains "HUMAN_IDENTITY_INFERENCE_DETECTED" if {
  object.get(object.get(input, "boundaries", {}), "human_identity_inferred", null) != false
}

deny contains "HUMAN_PRESENCE_INFERENCE_DETECTED" if {
  object.get(object.get(input, "boundaries", {}), "human_presence_inferred", null) != false
}

deny contains "MERGE_AUTHORITY_INFERENCE_DETECTED" if {
  object.get(object.get(input, "boundaries", {}), "merge_authority_inferred", null) != false
}

required_artifacts := {
  "attestation.intoto.json",
  "prov.jsonld",
  "ro-crate/ro-crate-metadata.json",
  "inspect/task-manifest.json",
  "inspect/dataset.jsonl",
  "openssf/scorecard-crosswalk.json",
}

deny contains "MISSING_DERIVATION_HASH" if {
  some name in required_artifacts
  not object.get(object.get(input, "artifact_digests", {}), name, "")
}

allow if {
  count(deny) == 0
}
