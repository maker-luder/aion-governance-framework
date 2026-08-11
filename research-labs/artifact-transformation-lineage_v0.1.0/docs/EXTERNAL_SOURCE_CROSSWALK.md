# External Source Crosswalk — OpenLineage + in-toto → AION Artifact Transformation Lineage

## Fixed source snapshots

### OpenLineage

- Repository: `OpenLineage/OpenLineage`
- Commit: `c54b98bd6666dfd8a7087f4f9793538357a677b9`
- Reviewed file: `website/docs/spec/object-model.md`
- Blob: `f72cef5cda309d5baaafb5e69a663e4f0abe1134`
- License: Apache-2.0

Selected public concepts: design-time metadata is distinct from run-time observations; Jobs consume/produce Datasets; each Run is a distinct occurrence with its own state transitions.

### in-toto

- Repository: `in-toto/in-toto`
- Commit: `a8ce9ee2125ae5a4b041a4e37cc1cf10eed0da6b`
- Reviewed file: `in_toto/models/link.py`
- Blob: `7ef05ec12099e2d1f16e9685f015c52754176359`
- License: Apache-2.0

Selected public concepts: a performed supply-chain step can record materials, products, command, byproducts and environment with artifact hashes.

## AION transformation

| Public concept | AION clean-room treatment |
|---|---|
| Job | `TransformationJob` |
| design-time job metadata | `TransformationPlan` |
| Run / RunEvent | `TransformationRunEvent` + `TransformationLedger` |
| input Dataset/material | `ArtifactRef` in `materials` |
| output Dataset/product | `ArtifactRef` in `products` |
| artifact hash | SHA-256-only fail-closed reference |
| command | record-only tuple; never executed by this module |
| environment | sanitized mapping before persistence |
| run states | START / COMPLETE / FAIL with ordered validation |

## Deliberately not imported

- no OpenLineage client/server/runtime;
- no in-toto Python package or signing implementation;
- no external schema copied;
- no external result or certification claim;
- no canonical promotion authority.
