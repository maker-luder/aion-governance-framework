# Conversational attention, turn-taking, and multi-agent coordination — 2026-09-13

Status: `RESEARCH_REFERENCE / DOCUMENTATION_ONLY / DRAFT`
Canonical effect: `NONE`
Deployment: `FALSE`
Executable implementation: `NONE`
Codex / ChatGPT Work implementation authorization: `NONE`
Merge authorization: `NONE`

## 1. Purpose

This note records a Human-side observation and a cross-domain research question that emerged from a real group-chat interaction.

The motivating question is not whether a person has a legal or moral right to speak. It is narrower:

> Can a high-density topic occupy enough shared conversational attention and floor time that other participants remain technically free to speak but experience practical difficulty entering, redirecting, or sustaining a different topic?

A second question follows:

> Does this Human-side coordination problem provide a useful analogy for multi-agent speaker selection, orchestration, attention management, and quality control?

This note does not treat a personal social event as scientific proof. It uses the event only as a hypothesis source.

## 2. Provenance

### HUMAN_OWNER_ORIGINAL

The Human Owner observed that:

- while discussing a dense programming / AI topic in a group chat, other participants reported that they could not easily enter the conversation or change the topic;
- no explicit prohibition prevented others from speaking;
- the Human Owner did not intend to monopolize the group and considered topic switching permissible;
- the resulting question was whether a high-attention / high-information topic can create a practical conversational bottleneck even without explicit coercion;
- the Human Owner independently connected this to multi-agent systems and asked whether a leader / orchestrator may sometimes be needed to integrate competing conversational trajectories;
- the Human Owner further asked whether this mechanism is more relevant to quality management and coordination than to AI subjectivity.

### CHATGPT_TEACHER_FORMALIZATION

The Teacher formalized the candidate mechanism as a distinction among:

```text
FORMAL_SPEAKING_PERMISSION
!= PRACTICAL_TURN_ACCESS
!= SHARED_ATTENTION_AVAILABILITY
!= TOPIC_SWITCHABILITY
```

and proposed a bounded working construct:

```text
SHARED_CONVERSATIONAL_ATTENTION_BOTTLENECK
= CHATGPT_TEACHER_WORKING_TERM
NOT_A_VALIDATED_PSYCHOLOGICAL_DIAGNOSIS
```

The construct refers to a situation in which one conversational trajectory consumes enough shared processing / floor structure that alternative contributions become harder to insert or maintain, even though participants remain formally free to speak.

## 3. Human conversation evidence

### 3.1 Information overload can reduce participation

Nematzadeh et al. (2019), using large-scale Twitch chat data, found a transition from a conversational regime to an overload / cacophony regime as information load increased. Per-capita participation eventually decreased under high information load.

Source:
- PMID `31824736`
- DOI `10.1098/rsos.191412`

Bounded inference:

```text
MORE_INFORMATION_FLOW
CAN
-> REDUCE_PER_CAPITA_PARTICIPATION
UNDER_OVERLOAD_CONDITIONS
```

This does not prove that semantic depth alone causes conversational exclusion.

### 3.2 Group discussion can shift toward serial monologue

Fay, Garrod & Carletta (2000) found that small groups behaved more like interactive dialogue, while larger groups behaved more like serial monologue, where the dominant speaker had greater influence.

Source:
- PMID `11202493`
- DOI `10.1111/1467-9280.00292`

Research implication:

```text
GROUP_CONVERSATION_STRUCTURE
CAN_SHIFT
FROM DIALOGIC EXCHANGE
TO SERIAL_MONOLOGUE-LIKE FLOW
```

This suggests that conversational accessibility depends on interaction structure, not merely formal permission to speak.

### 3.3 Turn-taking itself has cognitive cost

Conversation research shows that listeners often begin planning responses while still processing an ongoing turn. Parallel listening and response planning can increase cognitive load and reduce processing of later information.

A 2024 multimodal-information-density study summarizes this literature and notes the cognitive tradeoff between processing the current speaker and planning the next turn.

Source:
- DOI `10.1080/0163853X.2024.2413314`

Related multi-talker attention research reports measurable costs when attention must switch between speakers, especially for more complex questions.

Sources:
- PMID `31147609`
- PMC `PMC6542845`
- PMC `PMC4403343`

Bounded inference:

```text
LISTENING
+
RESPONSE_PLANNING
+
ATTENTION_SWITCHING
= NONZERO_COGNITIVE_COST
```

Therefore a dense, rapidly developing topic may raise the cost of entering the conversational floor without creating any literal prohibition.

### 3.4 Participation inequality is not identical to intentional suppression

Small-group research shows that floor time and interruptions can become unequally distributed through emerging conversational roles and status / participation dynamics.

Sources include:
- Meeker (2019), DOI `10.1016/j.ssresearch.2019.102367`;
- Cannon, Robinson & Smith-Lovin (2019), DOI `10.1177/2378023119849347`.

Important boundary:

```text
UNEQUAL_FLOOR_ACCESS
!= INTENTIONAL_CENSORSHIP
!= PROOF_OF_AGGRESSION
```

This is especially relevant to the motivating observation.

## 4. What the current evidence does NOT establish

The evidence does not justify the universal claim:

```text
HIGH_INFORMATION_DENSITY
-> PEOPLE_CANNOT_SPEAK
```

Nor does it establish that the Human Owner's particular group-chat episode was caused by one mechanism.

Competing explanations include:

- information / cognitive overload;
- topic-specialization mismatch;
- social deference;
- conversational habit;
- group size;
- asynchronous chat pacing;
- message length;
- consecutive-message frequency;
- perceived expertise / status;
- reluctance to interrupt;
- desire not to derail the existing topic;
- group-specific norms;
- interpersonal conflict avoidance.

Therefore:

```text
SPECIFIC_CAUSE_IN_THIS_GROUP = NOT_ESTABLISHED
```

## 5. Multi-agent systems crosswalk

The Human-side observation maps surprisingly well to current multi-agent engineering problems.

### 5.1 Group chat requires speaker selection

Microsoft Agent Framework's Group Chat orchestration explicitly uses an orchestrator to determine which agent speaks next and to coordinate conversation flow. Supported strategies include round-robin, prompt-based selection, and custom context-sensitive speaker selection.

Source:
- Microsoft Agent Framework documentation, 2026.

Relevant engineering distinction:

```text
ALL_AGENTS_HAVE_CAPABILITY_TO_SPEAK
!=
ALL_AGENTS_SHOULD_SPEAK_SIMULTANEOUSLY
```

### 5.2 Shared context does not solve turn allocation

A multi-agent group may share the same history yet still require a control policy for:

- speaker selection;
- ordering;
- termination;
- role coverage;
- topic transitions;
- context synchronization.

Therefore:

```text
SHARED_CONTEXT
!= COORDINATED_CONVERSATION
```

### 5.3 Orchestrator is one pattern, not a universal requirement

A centralized leader is not always necessary. Alternatives include:

- round-robin scheduling;
- deterministic transition graphs;
- peer handoff;
- dynamic speaker selection;
- hierarchical planning;
- decentralized protocols.

Hence:

```text
COORDINATION_REQUIRED
!= CENTRAL_LEADER_ALWAYS_REQUIRED
```

The Human-side analogy therefore supports a research question about coordination policy, not a blanket leadership claim.

## 6. NASA crosswalk: CRM / SFRM / automated teammates

NASA's Crew Resource Management tradition is highly relevant because it treats communication as part of operational safety rather than merely social etiquette.

### 6.1 Communication is a coordination resource

NASA research describes crew communication as supporting:

- information transfer;
- team / task management;
- shared problem solving;
- decision making;
- coordination.

Source:
- Kanki & Connors, NASA Ames, `From Crew Communication to Coordination: A Fundamental Means to an End`, NTRS document `20020064470`.

### 6.2 CRM integrates attention, workload, leadership, and communication

NASA evidence reports describe CRM / Spaceflight Resource Management as involving interactions among:

- situation awareness;
- self-awareness;
- communication;
- team dynamics;
- attention demands;
- decision making;
- leadership;
- adaptability;
- assertiveness;
- workload.

Source:
- NASA evidence report `20210012912`.

This is directly relevant to the current research question because it rejects the idea that communication quality can be evaluated independently of workload and attention allocation.

### 6.3 CRM for automated teammates

NASA research on `Crew Resource Management for Automated Teammates` explicitly adapts CRM concepts to automation as a teammate.

Relevant features include:

- mutual performance monitoring;
- workload redistribution;
- team leadership;
- task-related assertiveness;
- adaptability;
- bringing forward relevant information even when not explicitly requested.

Source:
- NTRS `20180004774`.

Important engineering translation:

```text
GOOD_TEAM_COORDINATION
= NOT_JUST_CORRECT_INDIVIDUAL_OUTPUTS
```

A system can contain individually capable participants and still fail through coordination, workload allocation, or communication structure.

## 7. NIST / human-AI teaming crosswalk

NIST's AI RMF roadmap explicitly identifies guidance on human-AI teaming as a research need and states that team configuration should be studied to reduce harms and improve oversight.

Source:
- NIST AI RMF Roadmap.

NIST materials also distinguish communication, coordination, and collaboration in human-robot / human-AI teaming and identify team-level measurement as necessary.

Relevant distinction:

```text
INDIVIDUAL_AGENT_PERFORMANCE
!= TEAM_PERFORMANCE
```

NIST's 2026 AI-for-Manufacturing materials further identify `multi-agent system coordination and safety` as a standards / measurement gap.

This is a strong external anchor for treating coordination as a quality object in its own right.

## 8. AISI / MSIT terminology clarification

The Human Owner recalled approximate acronyms including `MSIT` and `AIMST`.

Current search supports:

```text
MSIT = Ministry of Science and ICT, Republic of Korea
CONFIRMED_REAL_ORGANIZATION

AISI = AI Safety / Security Institute
CONFIRMED_RELEVANT_ACRONYM

AIMST = NO_RELEVANT_MATCH_CONFIRMED_IN_CURRENT_SEARCH
```

Korea's MSIT launched an AI Safety Institute following the AI Seoul Summit and describes functions including AI risk identification, safety evaluation methodology, and mitigation.

The UK AI Security Institute (AISI) conducts research on advanced-AI evaluation, control, autonomy, human influence, and multi-agent AI control.

Japan AISI's 2026 evaluation guide added agent-specific evaluation perspectives including `observation and control`, autonomous behavior, and interaction with external environments.

The repository should therefore preserve all three acronyms distinctly rather than collapse them:

```text
NIST != MSIT != AISI
```

If the Human Owner later identifies the intended remembered acronym, provenance should be corrected without rewriting the historical uncertainty.

## 9. AISI multi-agent control relevance

UK AISI's 2026 `Multi-Agent AI Control: Distributed Attacks Hamper Per-Instance Monitors` found that distributed coordination among multiple agents can make per-instance monitoring less effective; an explicit planner amplified the fragmentation effect in their test setting.

Source:
- AISI, 2026-07-08.

This is not about conversational politeness. It is important because it shows a general control principle:

```text
SYSTEM_LEVEL_COORDINATION
CAN_CREATE_FAILURE_MODES
NOT_VISIBLE_AT_SINGLE_AGENT_LEVEL
```

Therefore the repository's quality line should not assume:

```text
EACH_AGENT_LOOKS_OK
-> TEAM_BEHAVIOR_IS_OK
```

## 10. Quality-management implications

The current synthesis suggests that the repository should distinguish content quality from coordination quality.

### 10.1 New candidate quality class

```text
COORDINATION_QUALITY
!= CONTENT_QUALITY
```

Candidate failure modes include:

- one speaker / agent monopolizes turns unintentionally;
- required specialist never receives a turn;
- topic transition requests are repeatedly missed;
- shared context grows but role coverage shrinks;
- multiple agents repeat the same line instead of introducing counterevidence;
- monitor evaluates each agent independently while missing team-level behavior;
- workload accumulates on one participant;
- no termination / handoff condition exists;
- important dissent cannot enter the active conversational floor.

### 10.2 Candidate NCR condition

A coordination NCR should not be opened merely because participation is unequal.

It becomes a candidate NCR only when a defined process requirement exists and is violated.

Example:

```text
REQUIREMENT:
all critical roles must have an opportunity to contribute before release

OBSERVATION:
reviewer role never receives a turn

-> COORDINATION_NONCONFORMANCE_CANDIDATE
```

But:

```text
ONE_AGENT_SPEAKS_MORE
WITHOUT_REQUIREMENT_VIOLATION
!= NCR
```

### 10.3 Meta-QA question

Before diagnosing domination or suppression, QA should ask:

```text
IS_THE_FAILURE:
- content?
- attention allocation?
- speaker selection?
- workload?
- role design?
- topic-transition protocol?
- group norm?
- monitoring granularity?
```

This prevents a social observation from being prematurely moralized or overgeneralized.

## 11. Four-Domain mapping

### DOMAIN_1_HUMAN_CONSTRUCT

Candidate Human-side constructs:

- conversational floor;
- attention allocation;
- participation accessibility;
- cognitive load;
- topic switching;
- perceived ability to interrupt;
- coordination fairness.

Boundary:

```text
HUMAN_CONVERSATIONAL_DIFFICULTY
!= MACHINE_SUBJECTIVITY_EVIDENCE
```

### DOMAIN_2_MACHINE_QUESTION

Ontology-neutral questions:

- How is next-speaker selection determined?
- How much shared context does each agent receive?
- Can a dormant role request a turn?
- Can a topic-transition signal preempt the current trajectory?
- Is there a coordination state distinct from individual agent state?
- Does a planner / manager become a single point of failure?

### DOMAIN_3_ENGINEERING_OPERATION

Possible future evaluations:

- round-robin vs adaptive orchestrator;
- centralized vs decentralized speaker selection;
- full shared context vs scoped context;
- high-density single-topic runs vs mixed-topic runs;
- presence / absence of explicit topic-switch requests;
- presence / absence of dissent / reviewer role;
- per-agent monitoring vs system-level monitoring;
- measure turn concentration, role coverage, topic-switch latency, unresolved requests, repeated content, and termination quality.

No experiment is authorized by this note.

### DOMAIN_4_GOVERNANCE_INTERPRETATION

Possible governance boundaries:

```text
SPEAKER_DOMINANCE
!= INTENTIONAL_SUPPRESSION

TURN_ACCESS_FAILURE
!= RIGHTS_VIOLATION_BY_DEFAULT

ORCHESTRATOR_SELECTION
!= EPISTEMIC_AUTHORITY

CENTRAL_COORDINATION
!= CENTRALIZED_TRUTH

BALANCED_PARTICIPATION
!= CORRECTNESS

TEAM_COHERENCE
!= TEAM_VALIDITY

WORKFLOW_STABILITY
!= SUBJECTIVITY
```

## 12. Relationship to the repository's subjectivity program

This line is currently more useful for quality management, human-AI teaming, and multi-agent control than for the central subjectivity question.

Potential indirect value:

- prevents apparent multi-agent coherence from being mistaken for shared subjectivity;
- separates relational / conversational continuity from system-level coordination;
- creates better controls for agent-group experiments;
- improves interpretation of collective behavior.

Standing boundary:

```text
MULTI_AGENT_COORDINATION
!= SHARED_MIND

SHARED_CONTEXT
!= SHARED_CONSCIOUSNESS

COORDINATED_BEHAVIOR
!= SUBJECTIVITY
```

## 13. Current research hypothesis

### JOINT_RESEARCH_HYPOTHESIS

Following Human Owner observation and Teacher formalization:

> In group communication, a high-demand conversational trajectory may reduce practical turn accessibility by consuming shared attention, processing capacity, and floor structure without explicitly restricting anyone's formal ability to speak. Analogous coordination bottlenecks may arise in multi-agent systems, where speaker selection, context allocation, monitoring granularity, and orchestration become quality-management variables distinct from individual response correctness.

Status:

```text
HUMAN_SIDE_MECHANISM = PLAUSIBLE / NOT_CAUSALLY_ESTABLISHED_FOR_THIS_GROUP
MULTI_AGENT_ANALOGY = METHOD_RELEVANT
QUALITY_MANAGEMENT_RELEVANCE = HIGH
SUBJECTIVITY_RELEVANCE = INDIRECT
EXECUTABLE_IMPLEMENTATION = NONE
SCIENTIFIC_DISPOSITION = HOLD
```

## 14. Candidate future implementation — NOT AUTHORIZED

After a separate fresh Human Owner instruction, Codex / ChatGPT Work may review whether a minimal coordination-quality harness is justified.

Candidate components only:

1. speaker-selection policy interface;
2. role-coverage checker;
3. topic-switch request / acknowledgement event;
4. turn-concentration metric;
5. unresolved-request detector;
6. system-level monitor in addition to per-agent monitors;
7. coordination NCR trigger only for explicit requirement violations;
8. comparison of centralized and decentralized orchestration;
9. explicit stop / handoff conditions;
10. `NO_IMPLEMENTATION_YET` remains acceptable.

```text
CODEX_WORK_AUTHORIZATION = NONE
MERGE_AUTHORIZATION = NONE
MAIN_WRITE = NO
```
