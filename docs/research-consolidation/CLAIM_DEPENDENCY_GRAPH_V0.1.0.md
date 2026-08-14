# AION Claim Dependency Graph v0.1.0

> This graph describes **epistemic and engineering dependencies**, not execution authority. An edge means that one artifact supplies a method, input, validation surface, boundary or review context to another; it does not mean that the upstream artifact proves the downstream claim.

## Graph

```mermaid
flowchart TD
  WP[Whitepaper primary evidence architecture]\n  FD[Four-Domain repository crosswalk]\n  P1[P1 temporal correction evaluation primitives]
  P2[P2 Packet C retrieval provenance T2/T3]
  FX[P2 synthetic fixture A]
  T2[P2 compact tests and compile check]
  RT[AION Runtime v0.2 research substrate]
  G1[G1 language capability research substrate]
  P5[P5 hypothesis replication falsifier lifecycle]
  EA[Existing evidence admission schema/validator]
  FM[P2 falsifier matrix]
  DISP[Promotion readiness disposition]
  LIT[Primary-source literature]
  KIMI[Kimi external discovery intake]
  META[Meta review directives]
  SCOPE[Existing Research Scope Lock]
  HIST[Historical records and superseded snapshots]

  WP --> FD
  WP --> P1
  WP --> P2
  FD --> P1
  P1 --> P2
  P2 --> FX
  P2 --> T2
  P2 -. explicit non-integration boundary .-> RT
  P2 -. may be evaluated under method; no current edge .-> G1
  LIT --> FD
  LIT --> P2
  KIMI --> LIT
  META --> FD
  META --> P2
  P5 --> FM
  T2 --> FM
  EA --> DISP
  P2 --> EA
  FM --> DISP
  SCOPE --> FD
  SCOPE --> P2
  SCOPE --> G1
  HIST -. preserved provenance .-> DISP
```

## 1. Dependency edges

| Edge | Relation | What is established | What is not established |
|---|---|---|---|
| `WP -> FD` | method foundation | Four-Domain transforms constructs into questions, operations and governance controls under the standing evidence method | It does not prove any subjectivity claim |
| `WP -> P2` | scientific-method constraint | P2 must preserve alternative explanations, provenance, admissibility and claim scope | P2 is not a whitepaper result |
| `FD -> P1` | research decomposition | P1 materializes temporal, correction and evaluation gaps identified by the workbench | P1 is not production memory or a formal experiment |
| `P1 -> P2` | executable research dependency | P2 composes P1 correction, temporal and evaluation primitives | P2 does not inherit P1 authority or scientific validity |
| `P2 -> fixture/test` | implementation-to-evidence | The fixture and five tests exercise deterministic retrieval, fail-closed provenance, T2/T3 composition and continuity nonclaim | Test success is not scientific validation |
| `P2 -> Runtime v0.2` | explicit boundary | P2 remains model-independent and does not integrate, mutate or call Runtime v0.2 | No runtime evidence is claimed by P2 |
| `P2 -> G1` | no current implementation edge | G1 may later be evaluated as a parallel substrate under the Four-Domain method | Four-Domain does not depend on G1 and G1 does not establish subjectivity |
| `P5 -> falsifier/disposition` | governance substrate | P5 records hypothesis lifecycle, disagreement, replication state and falsifier decisions without majority-truth collapse | P5 does not make the P2 result true |
| `literature -> P2` | methodological translation | LongMemEval, MemoryAgentBench, MemEvoBench, Memora, PROV-O and MCP supply concepts for evaluation/provenance/context boundaries | External papers do not prove AION behavior |
| `Kimi -> literature` | discovery provenance | Kimi identifies leads retained in the intake | Kimi is not a primary source, replication or authority |
| `Scope Lock -> all research` | existing governance constraint | Existing checker enforces research object, roles, non-claim blocks and growth boundary | This convergence package does not replace or duplicate Scope Lock |
| `evidence admission -> disposition` | evidence gate | Existing schema/validator can validate a bounded research record with local references and canonical NONE | PASS is not acceptance, promotion or IV&V |

## 2. Four-Domain ↔ G1 decision

The graph deliberately contains **no claim-bearing edge** from G1 to Four-Domain scientific conclusions. G1 is a language-capability candidate with `RESEARCH_PROPOSALS_REGISTERED`, `QA_HOLD`, `canonical_effect=NONE`, and no identity, subjectivity, memory, tool, release or canonical authority. Four-Domain is the method that may later evaluate G1 or another substrate; it is not downstream of G1.

The only safe future relation is:

```text
FOUR_DOMAIN_METHOD
    -> pre-registered evaluation of a named G1 capability artifact
    -> bounded runtime/fixture evidence
    -> evidence admission
    -> falsifier and human review
```

That future relation is **not currently implemented** and remains `HOLD`.

## 3. Graph invariants

```text
TEST_PASS != SCIENTIFIC_VALIDATION
CI_SUCCESS != THEORY_CONFIRMATION
RUNTIME_MATURITY != SUBJECTIVITY_EVIDENCE
LITERATURE_ALIGNMENT != REPLICATION
KIMI_REVIEW != PRIMARY_SOURCE
PROVENANCE_RELATION != IDENTITY_RELATION
PERSISTENCE != AUTHORITY
COMMON_ORIGIN != SAME_IDENTITY
```
