# Interoperability mapping notes

This document records intentionally narrow mappings. The adapters must not infer semantics that the AION source schema does not structurally contain.

| AION surface | Interop view | Boundary |
| --- | --- | --- |
| `provenance.entities` | `prov:Entity` | entity presence is not identity proof |
| `provenance.activities` | `prov:Activity` | activity presence is not mechanism proof |
| `provenance.agents` | `prov:Agent` | agent label is not proof of physical or conceptual identity |
| `provenance.derived_from` | `prov:wasDerivedFrom` on source record | preserves declared derivation only |
| `provenance.attributed_to` | `prov:wasAttributedTo` on source record | attribution is not independent authorship proof |
| `provenance.associated_with` | opaque `aion:declaredAssociatedWith` | no pairwise association is invented |
| evidence record + artifacts | RO-Crate metadata graph rooted at bundle root | external source remains hash-bound; generated payload stays inside crate root |
| source SHA + source commit + output digests | in-toto Statement | unsigned derivation record only |
| interop manifest boundaries | OPA input / Rego | policy decision is not truth or authority |
| claim + expected outcomes + evidence metadata | Inspect `Sample` JSONL | static dataset export only |
| repository-local security/CI evidence | OpenSSF Scorecard-aligned crosswalk | crosswalk is not a Scorecard run, score, certification, or hosted-state proof |

## Four-Domain bridge

The optional Four-Domain bridge is an upstream materialization step, not a seventh interoperability format. It converts one exact preserved Four-Domain crosswalk snapshot into a schema-valid AION `research_evidence_record_v0.2.0`, which then enters the unchanged interoperability pipeline.

```text
review/four-domain-research-materialization
@ f654b5032ebc45058a64e81d409149ee7ea4bfbe
        |
        | exact artifact + Git blob identity
        v
Four-Domain bridge descriptor
        |
        v
AION research evidence record (result_status = HOLD)
        |
        v
existing AION validator
        |
        v
PROV / RO-Crate / in-toto / OPA / Inspect / OpenSSF
```

v0.1.0 is pinned to `FOUR_DOMAIN_REPOSITORY_CROSSWALK.md` at Git blob `7e55741b85b27d383b4b721b834b1744c6c03fb9`. The bridge does not resolve the live research branch tip and does not fetch the source artifact over the network. The exact source commit and blob identity remain inside the hash-bound AION source evidence record.

The bridge deliberately emits `result_status = HOLD`: it records a historical repository mapping and does not present that mapping as a newly executed experiment or completed scientific result.

```text
FOUR_DOMAIN_SOURCE != MAIN_CANONICAL_STATE
DERIVATION != MERGE
REFERENCE != PROMOTION
INTEROP_EXPORT != RESEARCH_RESTART
```

## Non-lossy AION fields

The interoperability views are not a replacement schema. Fields such as `observation`, `mechanism`, `interpretation`, competing hypotheses, limitations, claim ladder, preregistration, and nonclaims remain authoritative in the original AION evidence record even when only a subset is projected into a particular external format.

The Scorecard crosswalk is additionally repository-scoped rather than research-record-scoped. Its inclusion in the bundle records the local engineering context at the exact inspected head; it does not change the scientific status of the source evidence record.

## RO-Crate root rule

The complete generated interoperability output directory is the RO-Crate root. `ro-crate-metadata.json` therefore sits beside top-level payload such as `prov.jsonld`, while nested payload such as `opa/input.json`, `inspect/dataset.jsonl`, and `openssf/scorecard-crosswalk.json` remains inside that same root. No generated payload uses a `../` identifier to escape the crate root.

The authoritative AION source evidence record is not copied into the crate. It is represented by an absolute hash-derived URN and remains an external source entity. This preserves provenance without implying that the source file is crate-local payload.

## Hash construction order

| Layer | Hash-bound content | Deliberate exclusions |
| --- | --- | --- |
| RO-Crate | source record plus PROV, Inspect task/dataset, and OpenSSF crosswalk digests | its own metadata, later attestation, later OPA input, and later manifest |
| in-toto | source SHA-256, exact Git SHA-1, primary outputs, and RO-Crate metadata | its own unsigned Statement, later OPA input, and later manifest |
| OPA input | the pre-OPA derivation digest set it evaluates | its own digest |
| manifest | every generated output except the manifest | manifest self-hash only |

RO-Crate still represents every non-metadata bundle artifact in `hasPart`; files unavailable for non-circular hashing at that stage have no fabricated digest. `openssf/scorecard-crosswalk.json` is included in RO-Crate, in-toto, and final manifest binding.

```text
EXPORT_PROJECTION != SOURCE_REPLACEMENT
FORMAT_COMPATIBILITY != SEMANTIC_EQUIVALENCE
SCORECARD_CROSSWALK != SECURITY_CERTIFICATION
OBSERVATION != MECHANISM != INTERPRETATION
OBSERVATION != MECHANISM != PHENOMENAL_EXPERIENCE
```
