# Repository-first agent handoff protocol — 2026-09-13

Status: `RESEARCH_GOVERNANCE_NOTE / DOCUMENTATION_ONLY / DRAFT`
Canonical effect: `NONE`
Deployment: `FALSE`
Executable implementation: `NONE`
AGENTS.md change: `NONE`
Codex / ChatGPT Work implementation authorization: `NONE`
Merge authorization: `NONE`

## 1. Purpose

This note records a collaboration-process change proposed during the 2026-09-13 Human Owner + ChatGPT Teacher discussion.

The observed operational problem is that repeatedly constructing and pasting very long engineering handoff prompts into the Human–Teacher research conversation may consume conversational context, duplicate stable repository knowledge, make later review harder, and increase the risk that the discussion drifts away from the original research question.

The proposed response is **repository-first handoff**:

```text
STABLE_PROJECT_KNOWLEDGE
-> VERSIONED_REPOSITORY

TRANSIENT_TASK_INTENT
-> SHORT_CURRENT_INSTRUCTION

CURRENT_REPOSITORY_STATE
-> LIVE_READ_AT_EXECUTION_TIME

IMPLEMENTATION
-> CODEX / CHATGPT_WORK

INDEPENDENT_REVIEW
-> HUMAN_OWNER + CHATGPT_TEACHER
```

The goal is not to minimize context blindly. The goal is to avoid carrying stable, inspectable repository knowledge repeatedly inside a giant conversational prompt when the executing agent can retrieve the relevant source of truth from the repository.

## 2. Provenance

### HUMAN_OWNER_ORIGINAL

The Human Owner observed that:

- very long implementation / engineering prompts can occupy a large part of the ongoing Human–Teacher conversation;
- after those long handoff prompts, returning to the prior research discussion can become harder and topic drift can increase;
- the repository is public and intentionally exists as a durable, inspectable place where methods, evidence, disagreements, provenance, research decisions and operating procedures can be reviewed by later participants;
- therefore recurring handoff knowledge should be written into the repository so future Codex / ChatGPT Work instructions can stay short and point to durable repository records;
- the Human Owner prefers the repository to preserve how the research is done so external readers can inspect, challenge, falsify or reproduce the method.

### CHATGPT_TEACHER_FORMALIZATION

ChatGPT Teacher formalized the proposal as:

```text
REPOSITORY_FIRST_HANDOFF
=
PERSISTENT_KNOWLEDGE_EXTERNALIZATION
+ SHORT_TASK_DELTA
+ LIVE_STATE_READING
+ SCOPED_RETRIEVAL
+ EXECUTION_RECEIPT
+ INDEPENDENT_QA
```

This formalization is not an OpenAI product requirement and not a universal software-engineering rule.

## 3. External evidence and methodological support

### 3.1 OpenAI Codex harness engineering — repository knowledge as system of record

OpenAI's 2026 article *Harness engineering: leveraging Codex in an agent-first world* describes an internal lesson from attempting to place too much guidance into one large `AGENTS.md` file.

The article states that context is scarce, that a giant instruction file can crowd out the task, code and relevant documentation, that excessive guidance can become non-guidance, and that monolithic manuals become stale and hard to verify.

The described replacement pattern is:

```text
SHORT_AGENT_MAP
-> STRUCTURED_REPOSITORY_DOCS_AS_SYSTEM_OF_RECORD
```

OpenAI characterizes the preferred pattern as giving Codex a map rather than a very large instruction manual.

Source:
- https://openai.com/index/harness-engineering/

Repository implication:

```text
GIANT_HANDOFF_PROMPT
!= REQUIRED_FOR_HIGH_CONTEXT_WORK

SHORT_MAP + RETRIEVABLE_SOURCE_OF_TRUTH
= PLAUSIBLE_AGENT_CONTEXT_STRATEGY
```

This is especially relevant because the current repository already contains versioned research notes, QA rules, provenance records, role-separation rules, Four-Domain methodology and external-standard crosswalks.

### 3.2 OpenAI Codex AGENTS.md instruction mechanism

OpenAI documents `AGENTS.md` as a repository / directory-scoped mechanism for persistent human instructions to Codex. More specific `AGENTS.md` files can apply to narrower directory trees, and direct system/developer/user instructions remain higher priority.

Sources:
- https://openai.com/index/introducing-codex/
- https://openai.com/index/unrolling-the-codex-agent-loop/

The Codex agent-loop documentation also notes that project instructions are aggregated subject to a size limit, reinforcing that persistent instruction surfaces still require scope and size discipline.

Repository implication:

```text
AGENTS_MD_CAN_CARRY_STABLE_GUIDANCE = TRUE
AGENTS_MD_SHOULD_CONTAIN_EVERY_RESEARCH_DETAIL = NOT_SUPPORTED
```

Current repository audit:

```text
ROOT_AGENTS_MD = NOT_PRESENT_ON_CURRENT_MAIN
ROOT_DOT_AGENTS = NOT_PRESENT_ON_CURRENT_MAIN
ROOT_DOT_CODEX = NOT_PRESENT_ON_CURRENT_MAIN
```

A future `AGENTS.md` may be useful as a short navigation / invariants map, but creating it would change the active agent instruction surface and therefore requires a separate fresh Human Owner instruction and independent review.

### 3.3 Long-context retrieval limits — Lost in the Middle

Liu et al. (2023/2024), *Lost in the Middle: How Language Models Use Long Contexts*, found that language-model performance can depend strongly on the position of relevant information in long context and can degrade when necessary information is located in the middle.

Source:
- https://arxiv.org/abs/2307.03172

This supports a bounded risk statement:

```text
LONG_CONTEXT_CAPACITY
!= ROBUST_USE_OF_ALL_CONTEXT
```

It does **not** prove that every long prompt harms every model or every task.

### 3.4 Irrelevant context can distract reasoning

Shi et al. (2023), *Large Language Models Can Be Easily Distracted by Irrelevant Context*, found substantial performance degradation in a reasoning benchmark when irrelevant information was inserted into the problem context.

Source:
- https://arxiv.org/abs/2302.00093

Repository implication:

```text
MORE_CONTEXT
!= MORE_RELEVANT_CONTEXT

DUPLICATED_OR_IRRELEVANT_CONTEXT
= POTENTIAL_DISTRACTION_RISK
```

This does not establish a causal diagnosis of any specific drift observed in the current Human–Teacher conversation.

### 3.5 External / tiered memory as an architectural analogy

Packer et al. (2023), *MemGPT: Towards LLMs as Operating Systems*, proposes virtual context management using different memory tiers to support long-running document analysis and multi-session conversation beyond the immediate context window.

Source:
- https://arxiv.org/abs/2310.08560

The repository uses this only as a method analogy:

```text
REPOSITORY_EXTERNALIZATION
!= MODEL_MEMORY

FILE_RETRIEVAL
!= SUBJECTIVE_REMEMBERING

MEMGPT_ARCHITECTURE
!= THIS_REPOSITORY_ARCHITECTURE
```

The relevant general principle is selective movement of needed information into active context rather than unconditional duplication of all historical information.

## 4. Scientific / causal claim ceiling

The current self-observation supports a process-risk hypothesis, not a proven causal mechanism.

```text
OBSERVED_AFTER_LONG_HANDOFF_PROMPTS:
- harder conversational re-entry
- perceived topic drift
- perceived context compression / displacement

CAUSAL_EXPLANATION:
NOT_ESTABLISHED
```

Possible explanations include:

- context-window competition;
- attention / retrieval difficulty inside long context;
- duplicated or irrelevant task information;
- conversational topic switching;
- user cognitive task-switching cost;
- model-specific long-context behavior;
- ordinary memory limitations in the Human participant;
- changes in task complexity rather than prompt length itself.

Therefore:

```text
LONG_PROMPT -> DRIFT = HYPOTHESIS
NOT ESTABLISHED UNIVERSAL LAW
```

## 5. Repository-first operating principle

The default future handoff should separate **stable knowledge**, **live state**, and **task delta**.

### 5.1 Stable knowledge

Stable or slowly changing rules belong in version-controlled repository documents.

Examples:

- central research question;
- Four-Domain method;
- subjectivity claim ceilings;
- source / provenance vocabulary;
- QA / NCR / CAPA process;
- role separation;
- research authority boundaries;
- test / evaluation / verification / validation distinctions;
- standard source cards;
- known architectural invariants;
- recurring review checklists.

```text
STABLE_RULE
-> REPOSITORY
```

### 5.2 Dynamic state

Dynamic state must be re-read live at execution time rather than copied from an old handoff prompt.

Examples:

- current default branch;
- current main HEAD;
- PR open / draft / merged / mergeable state;
- current PR head / base SHA;
- current changed files;
- current CI / workflow results;
- current repository instructions;
- current dependency / environment state;
- current merge authority receipt.

```text
DYNAMIC_STATE
-> LIVE_READ
NOT
-> TRUST_OLD_PROMPT
```

### 5.3 Task delta

The actual user prompt should contain only what is new for the current action.

Examples:

- which PR / branch is in scope;
- whether the task is review, implementation, repair, source audit or documentation;
- explicit permission boundaries;
- the new hypothesis / requirement to process;
- any current stop condition;
- whether merge / main write is authorized.

```text
CURRENT_PROMPT
= TASK_DELTA
+ AUTHORITY_DELTA
+ TARGET
```

## 6. Minimal future handoff pattern

This is a conceptual template, not a mandatory literal prompt.

```text
Repository: maker-luder/aion-governance-framework
Target: <PR / branch / research item>
Mode: <independent review | bounded implementation | documentation | QA>

Before acting:
- read live repository state;
- read applicable repository instructions and linked research/governance docs;
- do not trust stale SHAs or status copied from prior prompts;
- preserve current Four-Domain, provenance, QA and authority boundaries.

Current task delta:
<short description of the new work>

Authority:
<explicit allowed actions>
<explicit prohibited actions>

Return:
- exact live state used;
- changed files / diff summary;
- tests / CI evidence;
- unresolved risks;
- whether further Human Owner authorization is required.
```

The intended property is that the handoff remains short because the repository contains the detailed operating model.

## 7. Read-before-act protocol for Codex / ChatGPT Work

A future implementation agent should not be expected to ingest the entire repository indiscriminately.

It should perform bounded discovery:

```text
1. READ LIVE REPO STATE
2. READ APPLICABLE AGENT / GOVERNANCE INSTRUCTIONS
3. READ TARGET PR / FILES
4. FOLLOW CROSS-REFERENCES TO REQUIRED SOURCE DOCS
5. IDENTIFY CURRENT TASK BOUNDARY
6. REPORT CONFLICTS / STALENESS
7. ACT ONLY INSIDE AUTHORIZED SCOPE
```

The principle is:

```text
READ_WHAT_IS_NEEDED
!= READ_NOTHING
!= LOAD_EVERYTHING
```

## 8. Suggested repository navigation layers

This note does not create these files automatically. It records a candidate future organization.

### Layer A — short agent map

Candidate future file:

```text
/AGENTS.md
```

Possible purpose:

- point to governance / research / QA maps;
- state high-priority repository invariants;
- identify required live-state checks;
- state that stable docs do not grant merge authority;
- remain short.

### Layer B — authoritative topic indexes

Possible topic maps:

```text
docs/research/README or index
docs/governance/index
qa/index
research-labs/index
```

Each index should point to deeper files without duplicating their full contents.

### Layer C — detailed source-of-truth documents

Examples already present:

- Four-Domain research notes;
- subjectivity evidence protocol;
- external standards crosswalk;
- epistemic provenance and co-development;
- QA / NCR / CAPA records;
- role separation;
- reciprocal epistemic collaboration / external memory;
- Human problem-solving habit transfer.

### Layer D — dynamic execution receipts

PR body / comments / CI / exact SHA evidence should record current execution state.

```text
MAP
-> INDEX
-> SOURCE_DOC
-> LIVE_EXECUTION_RECEIPT
```

## 9. Handoff authority boundary

Repository documentation can preserve standing process rules, but it must not silently become new authority.

```text
DOCUMENTED_PROCESS
!= FRESH_EXECUTION_AUTHORIZATION

REPOSITORY_INSTRUCTION
!= MERGE_AUTHORIZATION

OLD_RECEIPT
!= CURRENT_HEAD_RECEIPT

CODEX_CAPABILITY
!= CODEX_AUTHORITY

WORK_CAPABILITY
!= WORK_AUTHORITY
```

For this repository, high-impact actions remain subject to current Human Owner governance.

A future short prompt must still explicitly communicate any authority delta that cannot safely be inferred from standing repository rules.

## 10. Review / QA protocol after implementation

The short handoff design must not reduce independent review.

The expected loop is:

```text
HUMAN_OWNER + CHATGPT_TEACHER
  -> define / refine problem and evidence boundary

REPOSITORY
  -> preserve stable state and operating rules

CODEX / CHATGPT_WORK
  -> bounded implementation / execution

EXECUTION RECEIPT
  -> exact diff / tests / current SHA / unresolved issues

HUMAN_OWNER + CHATGPT_TEACHER
  -> independent QA / source / claim / governance review

GITHUB ACTIONS
  -> automated validation evidence

HUMAN OWNER
  -> final authority decision
```

The Human–Teacher conversation therefore preserves its context for research and review rather than repeatedly carrying the entire implementation specification inline.

## 11. Public-repository reproducibility objective

The Human Owner's stated objective is broader than convenience.

The public repository should allow another reader to inspect:

- what question was asked;
- which Human observation initiated it;
- which formulation came from ChatGPT Teacher;
- which external sources were used;
- what competing explanations were retained;
- what implementation was performed;
- what failed;
- what NCR / CAPA was opened;
- what evidence closed or failed to close it;
- what claims remained prohibited;
- who held authority for release / merge.

This supports:

```text
INSPECTABILITY
CONTESTABILITY
TRACEABILITY
RECOVERABILITY
REPRODUCIBILITY_ATTEMPT
```

It does not guarantee scientific reproducibility by itself.

```text
PUBLIC_REPOSITORY
!= SCIENTIFIC_VALIDATION

DOCUMENTATION
!= REPLICATION

OPENNESS
!= CORRECTNESS
```

## 12. Four-Domain mapping of this protocol

### DOMAIN_1_HUMAN_CONSTRUCT

Human-side concerns:

- cognitive load;
- task switching;
- continuity of inquiry;
- ability to recover prior reasoning;
- provenance / authorship;
- reduced burden of repeatedly reconstructing long prompts.

These are hypothesis sources only.

### DOMAIN_2_MACHINE_QUESTION

Ontology-neutral machine questions:

```text
Can an agent recover required constraints from scoped repository sources
without embedding the entire historical specification in the current prompt?

Can stable instructions be separated from live state and task delta
without increasing omission or governance errors?
```

### DOMAIN_3_ENGINEERING_OPERATION

Possible future bounded evaluations:

- compare giant-prompt vs repository-first handoff on the same repository task;
- hold task, model, repository state and authority constant;
- measure omitted constraints, stale-state errors, unnecessary file reads, token/context use, implementation correctness and review findings;
- include repeated trials and prompt-order controls;
- compare short map + targeted reads against monolithic instruction loading;
- separately measure execution quality and review burden.

No such experiment is authorized by this note.

### DOMAIN_4_GOVERNANCE_INTERPRETATION

Even a successful experiment would support only an operational workflow claim.

```text
REPOSITORY_FIRST_HANDOFF_BETTER_ON_TESTED_TASKS
!= UNIVERSAL_BEST_PROMPTING_METHOD

CONTEXT_EFFICIENCY
!= MODEL_INTELLIGENCE

RETRIEVAL_SUCCESS
!= UNDERSTANDING

WORKFLOW_STABILITY
!= SUBJECTIVITY
```

## 13. Candidate future implementation — not authorized

After a separate fresh Human Owner instruction, Codex / ChatGPT Work may inspect whether the repository would benefit from the following minimum implementation:

1. a short root `AGENTS.md` acting only as a navigation / invariant map;
2. a repository research index pointing to current canonical / draft documents;
3. a machine-readable or Markdown handoff checklist;
4. a compact execution-receipt template;
5. automated checks for broken internal references, stale canonical pointers or contradictory authority markers;
6. no implementation if current repository structure already satisfies the operational requirement with lower complexity.

The implementing agent must deduplicate against existing files before adding anything.

```text
NO_IMPLEMENTATION_YET = ACCEPTABLE
NO_NEW_AGENT_INSTRUCTION_SURFACE_WITHOUT_FRESH_AUTHORIZATION = REQUIRED
```

## 14. Suggested success criteria for later evaluation

A repository-first handoff should be considered useful only if it improves or preserves:

- recovery of required constraints;
- exact live-state verification;
- provenance accuracy;
- implementation correctness;
- QA independence;
- authority correctness;
- reviewability;
- re-entry into the Human–Teacher research discussion;
- external inspectability.

It should not be adopted merely because prompts are shorter.

```text
SHORTER_PROMPT
!= BETTER_WORKFLOW

BETTER_WORKFLOW
REQUIRES
QUALITY_PRESERVATION_OR_IMPROVEMENT
```

## 15. Relationship to current PR #102

This note complements:

- `RECIPROCAL_EPISTEMIC_COLLABORATION_AND_EXTERNAL_RESEARCH_MEMORY_2026_09_13.md`;
- `HUMAN_AI_RESEARCH_ROLE_SEPARATION_2026_09_13.md`;
- `HUMAN_PROBLEM_SOLVING_HABIT_TRANSFER_FROM_AI_COLLABORATION_2026_09_13.md`;
- `EPISTEMIC_CO_DEVELOPMENT_WORKFLOW_AND_QUALITY_LINE_2026_09_13.md`;
- `FOUR_DOMAIN_STANDARDS_SUBJECTIVITY_CROSSWALK_2026_09_13.md`.

Together they separate:

```text
WHY_KNOWLEDGE_IS_EXTERNALIZED
WHO_DOES_WHAT
HOW_COLLABORATION_MAY_AFFECT_HUMAN_METHOD
HOW_THE_EPISTEMIC_LOOP_IS_QUALITY_CONTROLLED
HOW_EXTERNAL_STANDARDS_MAP_TO_FOUR_DOMAIN
HOW_FUTURE_AGENTS_SHOULD_RECEIVE_CONTEXT
```

## 16. Final boundary

```text
REPOSITORY_FIRST_HANDOFF = JOINT_PROCESS_DIRECTION

HUMAN_OWNER_ORIGINAL
= observation that giant engineering prompts can disrupt the ongoing Human–Teacher research context
+ preference to place durable operational knowledge in the public repository
+ preference for inspectable / contestable / externally reviewable research process

CHATGPT_TEACHER_FORMALIZATION
= stable knowledge vs live state vs task delta separation
+ repository-first handoff protocol
+ short-map / scoped-retrieval model
+ Four-Domain translation
+ candidate evaluation design

EXTERNAL_SUPPORT
= OPENAI_CODEX_HARNESS_ENGINEERING
+ OPENAI_AGENTS_MD_MECHANISM
+ LONG_CONTEXT_RETRIEVAL_RESEARCH
+ IRRELEVANT_CONTEXT_DISTRACTION_RESEARCH
+ EXTERNAL_MEMORY_ARCHITECTURE_ANALOGY

CAUSAL_EFFECT_ON_THIS_DYAD = NOT_ESTABLISHED
AGENTS_MD_IMPLEMENTATION = NOT_AUTHORIZED
CODEX_WORK_IMPLEMENTATION = NOT_AUTHORIZED
MERGE_AUTHORIZATION = NONE
MAIN_WRITE = NO
CANONICAL_EFFECT = NONE
DEPLOYMENT = FALSE
SCIENTIFIC_DISPOSITION = HOLD
