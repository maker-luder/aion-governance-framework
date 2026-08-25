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
| evidence record + artifacts | RO-Crate metadata graph | package view only |
| source SHA + source commit + output digests | in-toto Statement | unsigned derivation record only |
| interop manifest boundaries | OPA input / Rego | policy decision is not truth or authority |
| claim + expected outcomes + evidence metadata | Inspect `Sample` JSONL | static dataset export only |
| repository-local security/CI evidence | OpenSSF Scorecard-aligned crosswalk | crosswalk is not a Scorecard run, score, certification, or hosted-state proof |

## Non-lossy AION fields

The interoperability views are not a replacement schema. Fields such as `observation`, `mechanism`, `interpretation`, competing hypotheses, limitations, claim ladder, preregistration, and nonclaims remain authoritative in the original AION evidence record even when only a subset is projected into a particular external format.

The Scorecard crosswalk is additionally repository-scoped rather than research-record-scoped. Its inclusion in the bundle records the local engineering context at the exact inspected head; it does not change the scientific status of the source evidence record.

```text
EXPORT_PROJECTION != SOURCE_REPLACEMENT
FORMAT_COMPATIBILITY != SEMANTIC_EQUIVALENCE
SCORECARD_CROSSWALK != SECURITY_CERTIFICATION
OBSERVATION != MECHANISM != INTERPRETATION
```
