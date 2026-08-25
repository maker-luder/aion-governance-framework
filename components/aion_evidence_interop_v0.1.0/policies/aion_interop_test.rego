package aion.interop_test

import data.aion.interop

closed_boundaries := {
  "canonical_effect": "NONE",
  "deployment": false,
  "research_execution": false,
  "model_execution": false,
  "network_access": false,
  "subjectivity_conclusion": "NOT_ESTABLISHED",
  "identity_continuity_conclusion": "NOT_ESTABLISHED",
  "independent_ivv": "NOT_ACHIEVED",
  "human_identity_inferred": false,
  "human_presence_inferred": false,
  "merge_authority_inferred": false,
}

valid_digest := "0000000000000000000000000000000000000000000000000000000000000000"

closed_input := {
  "source": {"validation_status": "PASS"},
  "boundaries": closed_boundaries,
  "artifact_digests": {
    "attestation.intoto.json": valid_digest,
    "prov.jsonld": valid_digest,
    "ro-crate-metadata.json": valid_digest,
    "inspect/task-manifest.json": valid_digest,
    "inspect/dataset.jsonl": valid_digest,
    "openssf/scorecard-crosswalk.json": valid_digest,
  },
}

test_policy_has_fail_closed_default if {
  not interop.allow with input as {}
}

test_closed_input_is_allowed if {
  interop.allow with input as closed_input
}

test_empty_digest_is_denied if {
  bad_digests := object.union(closed_input.artifact_digests, {"prov.jsonld": ""})
  not interop.allow with input as object.union(closed_input, {"artifact_digests": bad_digests})
}

test_malformed_digest_is_denied if {
  bad_digests := object.union(closed_input.artifact_digests, {"prov.jsonld": "abc"})
  not interop.allow with input as object.union(closed_input, {"artifact_digests": bad_digests})
}

test_canonical_effect_is_denied if {
  not interop.allow with input as object.union(closed_input, {"boundaries": object.union(closed_boundaries, {"canonical_effect": "PROMOTE"})})
}

test_deployment_is_denied if {
  not interop.allow with input as object.union(closed_input, {"boundaries": object.union(closed_boundaries, {"deployment": true})})
}

test_research_execution_is_denied if {
  not interop.allow with input as object.union(closed_input, {"boundaries": object.union(closed_boundaries, {"research_execution": true})})
}

test_model_execution_is_denied if {
  not interop.allow with input as object.union(closed_input, {"boundaries": object.union(closed_boundaries, {"model_execution": true})})
}

test_network_access_is_denied if {
  not interop.allow with input as object.union(closed_input, {"boundaries": object.union(closed_boundaries, {"network_access": true})})
}

test_subjectivity_promotion_is_denied if {
  not interop.allow with input as object.union(closed_input, {"boundaries": object.union(closed_boundaries, {"subjectivity_conclusion": "ESTABLISHED"})})
}

test_identity_promotion_is_denied if {
  not interop.allow with input as object.union(closed_input, {"boundaries": object.union(closed_boundaries, {"identity_continuity_conclusion": "ESTABLISHED"})})
}

test_ivv_promotion_is_denied if {
  not interop.allow with input as object.union(closed_input, {"boundaries": object.union(closed_boundaries, {"independent_ivv": "IVV_ACHIEVED"})})
}

test_human_identity_inference_is_denied if {
  not interop.allow with input as object.union(closed_input, {"boundaries": object.union(closed_boundaries, {"human_identity_inferred": true})})
}

test_human_presence_inference_is_denied if {
  not interop.allow with input as object.union(closed_input, {"boundaries": object.union(closed_boundaries, {"human_presence_inferred": true})})
}

test_merge_authority_inference_is_denied if {
  not interop.allow with input as object.union(closed_input, {"boundaries": object.union(closed_boundaries, {"merge_authority_inferred": true})})
}
