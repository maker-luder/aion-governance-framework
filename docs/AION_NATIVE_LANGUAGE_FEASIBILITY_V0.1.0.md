# AION Native Language Feasibility v0.1.0

**Status:** `ESTABLISHED_CANDIDATE / NON_EXECUTABLE`

**Feasibility decision:** `PROCEED_AS_CONSTRAINED_SEMANTIC_DSL`

**Working designation:** AION Native Language; its canonical permanent name remains `OWNER_DECISION_REQUIRED`.

**Canonical effect:** `NONE`

**Deployment:** `FALSE`

## 1. Decision

AION should not begin a general-purpose programming language. Repository evidence supports a **constrained, declarative, non-Turing-complete semantic DSL** that describes stable AION requirements and produces a validated, language-neutral semantic IR. It must not execute source, manufacture authority, replace existing Python, or freeze unresolved Event / Lineage / audit hash semantics.

The proposal has a narrow architectural purpose. Human-authored source can describe identity references, runtime references, provenance declarations, declared effect bounds, approval requirements, capability requirements, lifecycle requirements, and bounded memory-namespace declarations. Parsing and static semantic analysis can make these declarations more auditable and comparable than ad hoc host-language structures. External governed admission remains the only place where authority, capability grants, approval evidence, runtime mutation, canonical action, or execution may be established.

> **Source text is not authorization. AST is not authorization. Validated semantic IR is not authorization.**

## 2. Provenance and contribution boundary

| Role | Provenance statement |
|---|---|
| `HUMAN_OWNER_ORIGIN` | The Human Owner proposed a project-specific original AION programming / description language rather than an architecture implemented only through existing languages. |
| `CHATGPT_ARCHITECTURE_REFINEMENT` | The recommended first phase is a constrained semantic DSL, followed by AST and validated semantic IR, then future multi-parser conformance; governed runtime semantics remain a separately authorized future question. |
| `MANUS_CONTRIBUTION` | This milestone performs repository-grounded feasibility analysis, candidate language architecture, semantic eligibility classification, grammar/IR artifacts, threat analysis, and non-executable validation. |

This document does not rewrite historical authorship or attribute the original language direction to later implementation work.

## 3. Comparison of the five alternatives

| Option | Architectural value | Governance and security | Implementation / maintenance burden | Decision |
|---|---|---|---|---|
| A. Host languages + JSON Schema only | Retains current candidate contracts with no new source surface | Lowest new attack surface, but declarative architectural review remains scattered across schema, code, and prose | Lowest | Insufficient as the sole long-term authoring surface once stable cross-domain semantics need reviewable declarations |
| B. AION semantic IR only | Provides language-neutral machine representation and future adapter target | Strong for tooling; weak human authoring / review ergonomics without a source notation | Moderate | Necessary component, but incomplete as the only authoring model |
| C. Policy / contract DSL | Focuses tightly on rules and authority requirements | Strongly aligned to governance, but too narrow for runtime, provenance, and identity descriptions | Moderate | Viable subset, but unnecessarily limits the stable semantic surface |
| D. Constrained semantic DSL | Represents stable AION-specific requirements while preserving a language-neutral IR | Fail-closed, statically analyzable, auditable, and able to reject self-authorizing source forms | Moderate and bounded | **Selected candidate** |
| E. General-purpose AION programming language | Maximum expressiveness | Enlarges execution, parser, tooling, sandbox, supply-chain, and confused-deputy attack surfaces before core contracts are mature | Very high | Rejected for this milestone; a future separate program would need measurable justification |

The selected option is not a Python replacement and has no language-count objective. Its value is semantic precision around AION-specific declarations, not a new computational substrate.

## 4. Semantic eligibility matrix

| Domain | Current contract status | Language classification | Native syntax? | IR field? | External runtime evidence? | Authority implication | Stability / blocker |
|---|---:|---|---|---|---|---|---|
| Interop | `ESTABLISHED_CANDIDATE` | `IR_ONLY` | Only document language version | Yes | No | None | Reuse candidate profile; no independent DSL serialization rules |
| Identity | `ESTABLISHED_CANDIDATE` | `NATIVE_LANGUAGE_CONSTRUCT` | Yes: reference only | Yes | Yes: binding / ownership | Identifier never grants authority | Stable reference semantics; binding remains external |
| RuntimeContext completion | `ESTABLISHED_CANDIDATE` | `IR_ONLY` | No complete context syntax | External reference only | Yes | Context fields never self-bind authority | `memory_stream_id`, `event_lineage_id`, `canonical_state_reference`, and `genesis_root_id` remain external because their dependent semantics are not frozen |
| Effects | `PARTIAL` | `NATIVE_LANGUAGE_CONSTRUCT` | Yes: declarative bounds | Yes | Yes: actual result | Only `canonical_effect: none` is representable | Runtime-effect vocabulary remains bounded |
| Provenance | `ESTABLISHED_CANDIDATE` | `NATIVE_LANGUAGE_CONSTRUCT` | Yes: declaration / reference | Yes | Yes: evidence verification | Attribution is not approval | Stable as source-derived assertion with explicit uncertainty |
| Events | `PARTIAL` | `BLOCKED_BY_CONTRACT_GAP` | No persisted envelope syntax | No resolved envelope field | Yes | No authority | Exact envelope, ordering, and payload semantics unresolved |
| Lineage | `PARTIAL` | `BLOCKED_BY_CONTRACT_GAP` | No persisted hash / predecessor syntax | No resolved hash field | Yes | No authority | Runtime / audit genesis and framing diverge |
| Lifecycle | `END_TO_END_CANDIDATE / PYTHON_REFERENCE` | `NATIVE_LANGUAGE_CONSTRUCT` | Yes: requirement only | Yes | Yes: transition admission/outcome | Request never self-claims atomicity or success | Generic request/outcome is candidate; runtime outcome external |
| Memory namespace | `PARTIAL` | `NATIVE_LANGUAGE_CONSTRUCT` | Yes: owner-bound namespace declaration | Yes | Yes: access / mutation result | Namespace label cannot transfer ownership | Namespace distinction is stable; record/mutation semantics remain provisional |
| Memory record / mutation | `PARTIAL` | `PROVISIONAL` | No mutation execution syntax | Optional requirement only | Yes | Approval and persistence remain external | Conflict, tombstone, supersession, and portability need contracts |
| Governance | `PARTIAL` | `IR_ONLY` | No decision engine syntax | Yes: requirement reference | Yes | Policy evaluation external | GovernanceDecision / PolicyDecision contracts incomplete |
| Approval | `PARTIAL` | `NATIVE_LANGUAGE_CONSTRUCT` | Yes: required scope / target only | Yes | Yes: evidence and freshness | Cannot state `approval_satisfied` | Source requirement and external proof stay separated |
| Capability | `PARTIAL` | `NATIVE_LANGUAGE_CONSTRUCT` | Yes: required bounded capability only | Yes | Yes: admission result | Request is not grant | CapabilityAdmission contract remains incomplete |
| Tools | `PARTIAL` | `PROVISIONAL` | No invocation or execution syntax | Optional requirement reference | Yes | No tool authority | Tool request/result semantics not yet unified |
| Checkpoint | `PARTIAL` | `PROVISIONAL` | Requirement reference only | Optional | Yes | No recovery authority | Ownership / integrity / version semantics incomplete |
| Recovery | `PARTIAL` | `BLOCKED_BY_CONTRACT_GAP` | No execution syntax | No outcome semantics | Yes | No state restoration authority | Cross-language recovery contract not stable |
| Genesis | `PARTIAL` | `IR_ONLY` | No birth/selfhood constructs | Yes: reference | Yes | No personhood inference | Authorized binding only; semantics remain limited |
| Audit | `PARTIAL` | `PROVISIONAL` | No audit hash framing syntax | Optional declaration metadata | Yes | Audit is not authority | Audit and runtime hash profiles diverge |

## 5. Candidate native constructs

The v0.1 candidate language surface is deliberately small. It includes a document version header, `runtime` declaration, typed identity and runtime references, provenance declaration, memory-namespace declaration, lifecycle requirement, approval requirement, capability requirement, and effect declaration. An `operation` declaration may describe a request profile, but it cannot invoke a tool or execute a runtime action.

The following are **IR-only**: explicit interop-profile reference, IR version, normalized semantic identities, error-envelope mapping, source-location diagnostics, policy requirement references, and genesis references. They are meaningful to validated IR but do not need user-authored syntax in the first language surface.

The following remain **provisional**: memory record and mutation, governance policy, tool declarations, checkpoint requirement, audit metadata, and abstract event reference. The following are **blocked**: EventEnvelope shape, EventLineage hash framing, genesis predecessor, audit/runtime reconciliation, rehashing, migration behavior, recovery outcome, canonical write authority, and actual capability admission.

The first version explicitly **excludes** functions, variables, algebraic data types, pattern matching, iteration, recursion, modules, generics, concurrency, threads, async tasks, sockets, filesystem access, process spawning, dynamic import, evaluation, reflection, native calls, package download, plugin loading, and unrestricted networking. These are either `NOT_JUSTIFIED`, `CONTRARY_TO_LANGUAGE_PURPOSE`, `SECURITY_RISK`, or `REQUIRES_SEPARATE_PROGRAM`.

The lifecycle bridge is intentionally narrow: source `transition: start` maps to the existing request event type `runtime.started`, and source `transition: stop` maps to `runtime.stopped`. No lifecycle outcome, event sequence, event hash, derived state, or atomicity field enters v0.1 IR.

## 6. Source, AST, and validated IR boundary

Source records what a human wrote. AST records the parsed syntactic structure and source locations. Validated IR records normalized semantic meaning only after lexical validation, grammar validation, static semantic checks, version checks, effect checks, identity-reference checks where possible, and authority-requirement classification. Neither source, AST, nor validated IR contains a capability grant, verified approval, canonical write authorization, or runtime success.

Semantically equivalent source formatting, comments, and declaration layout should produce the same validated IR where the grammar permits. Raw source text is source-artifact evidence and must not be treated as runtime identity or canonical state.

## 7. Future implementation recommendation

A future implementation phase should begin with **one Python reference parser and semantic analyzer**, because it can reuse the current reference conformance environment. This is a recommendation about an implementation sequence, not an ownership claim over AION semantics. A Rust, Go, or TypeScript second implementation is not selected now; its future responsibility must be justified separately, and it must consume identical grammar/IR vectors and produce the same semantic outcomes.

A future general-purpose language is `NOT_JUSTIFIED`. The correct next engineering phase after Owner review would be a non-executing parser / semantic-analyzer program that emits only validated IR; production compilation, interpretation, VM design, runtime evaluation, adapters, or tool bridges require separate authorization.

## 8. Foundation conflicts and review boundary

No change to the current Interoperability Profile is proposed. The candidate DSL relies on its UTF-8, NFC admission, strict versioning, safe integer, strict JSON, deterministic-object-order, Error Envelope, and `canonical_effect = NONE` rules. The unresolved Event / Lineage / audit hash divergence is preserved as a `BLOCKED_BY_CONTRACT_GAP` boundary rather than a new language semantic.

The feasibility milestone should stop after the non-executable artifact set and review handoff. The next phase classification is `OWNER_DECISION_REQUIRED`: an Owner must explicitly authorize any reference parser, semantic analyzer implementation, cross-parser plan, runtime adapter, event/lineage migration, canonical expansion, or execution capability.

## References

[1]: AION_CROSS_LANGUAGE_CONTRACT_SURFACE_MAP_V0.1.0.md "Current contract-family topology and dependency graph"
[2]: AION_INTEROPERABILITY_PROFILE_V0.1.0.md "Current candidate interop rules and hash compatibility boundary"
[3]: ../schemas/individual_runtime_context_v0.1.0.schema.json "Individual Runtime Context schema"
[4]: ../schemas/individual_runtime_lifecycle_transition_request_v0.1.0.schema.json "Lifecycle Transition Request schema"
[5]: ../schemas/provenance_record.schema.json "Provenance Record schema"
