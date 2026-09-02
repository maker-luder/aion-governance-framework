# Zi Wei Dou Shu v0.1 verification record

## Immutable scope

```text
BASE_COMMIT=bb3e5e092c11a1b582a163422611308aaeab1f01
CORE_COMMIT=0199d3edb506cc0b85afca45880ba43df3481a43
PATCH_SHA256=8a08a3e8e9dce8497821605d6c0530b315d91c8df1edf1bc02a4cc8fc358dfd9
AI_SUBJECTIVITY_POSSIBILITY=CENTRAL_RESEARCH_QUESTION
NEW_CANONICAL_STATE_CHANNELS=NONE
CANONICAL_EFFECT=NONE
DEPLOYMENT=FALSE
ACTION_AUTHORITY=NONE
```

The implementation commit changes only a bounded comparison example, source
evidence, public indexes, third-party notice and a component-local CI workflow.
It does not alter the canonical subjectivity protocol, current semantic state,
the seven-state owner, the bounded inquiry loop or autonomous campaign owner.

## Baseline behavior

Command:

```powershell
git rev-parse bb3e5e092c11a1b582a163422611308aaeab1f01
```

Output and status (the machine-specific repository root in the command line is
normalized to `<REPOSITORY_ROOT>` so the public record contains no private
workstation path; all other output is literal):

```text
bb3e5e092c11a1b582a163422611308aaeab1f01
EXIT=0
```

Command:

```powershell
git cat-file -e "bb3e5e092c11a1b582a163422611308aaeab1f01:examples/zi-wei-dou-shu_v0.1.0"
```

Literal output and status:

```text
fatal: path 'examples/zi-wei-dou-shu_v0.1.0' exists on disk, but not in 'bb3e5e092c11a1b582a163422611308aaeab1f01'
EXIT=128
```

Baseline behavior is therefore the absence of a Zi Wei component and source
register.

## Modified deterministic behavior

Input: `examples/zi-wei-dou-shu_v0.1.0/fixtures/synthetic-lunar.json`.

Command:

```powershell
node -e "import('./examples/zi-wei-dou-shu_v0.1.0/src/index.js').then(async m=>{const fs=await import('node:fs/promises');const i=JSON.parse(await fs.readFile('./examples/zi-wei-dou-shu_v0.1.0/fixtures/synthetic-lunar.json','utf8'));const o=m.buildFactProfile(i);console.log(JSON.stringify({receipt:o.receipt.sha256,palaces:o.coverage.palaceCount,major:o.coverage.majorStarCount,transformations:o.coverage.transformationCount,layers:o.coverage.temporalLayers,core:o.boundaries.AI_SUBJECTIVITY_POSSIBILITY,canonicalEffect:o.boundaries.CANONICAL_EFFECT}))})"
```

Literal output and status:

```text
{"receipt":"f01bd61eb313cd99ec86dc79aca437291801cf060e77e8050ed6bc4fd5f5cabf","palaces":12,"major":14,"transformations":4,"layers":["decadal","age","yearly","monthly","daily","hourly"],"core":"CENTRAL_RESEARCH_QUESTION","canonicalEffect":"NONE"}
EXIT=0
```

Modified behavior is a deterministic, synthetic-only fact profile with 12
palaces, 14 primary stars, 4 transformations and six explicit-reference time
layers. It emits no interpretation or subjectivity promotion.

## Source acquisition and replay

Command:

```powershell
python scripts/fetch_ziwei_sources.py
```

Literal summary and status:

```text
source_count=7
download_status=PASS (7/7)
retained_snapshots=3
hash_only_discarded=4
IZTRO_NPM_SHA256=df7013db5260d548ed1359f5173089eab6a925d90e15b327235b10a1e0b0abb9
WIKISOURCE_DOWNLOAD_SHA256=4177fd28237bb22e122cb1121ef51ffc8768606c5948ad86efc4ce4eab073626
WIKISOURCE_REPOSITORY_SHA256=760c3a8e3eaa8bb21fb955c24c585d04f5f396b9653f2fbc061cb942dc1831b1
EXIT=0
```

Two consecutive runs produced the same manifest:

```text
FETCH_REPLAY_BEFORE=640fafffe74d232774d779281bda60005d4acc422f785f2a72bc52539c299b9a
FETCH_REPLAY_AFTER=640fafffe74d232774d779281bda60005d4acc422f785f2a72bc52539c299b9a
FETCH_REPLAY_MATCH=True
EXIT=0
```

## Test commands and literal results

```powershell
pnpm install --frozen-lockfile --ignore-scripts
pnpm test
```

```text
Already up to date
tests 8
pass 8
fail 0
EXIT=0
```

```powershell
python -m pytest -q examples/classical-western-astrology_v0.1.0/tests
python -m pytest -q examples/bazi-capability_v0.1.1/tests
```

```text
42 passed in 0.26s
EXIT=0
97 passed in 1.24s
EXIT=0
```

```powershell
pnpm audit --audit-level high
```

```text
No known vulnerabilities found
EXIT=0
```

The complete Windows repository test attempt was also retained rather than
weakened:

```powershell
python -m pytest -q tests
```

```text
90 passed, 5 failed
4 failures: WinError 1314 while tests attempted to create symlinks
1 failure: existing Windows path separator expectation in test_component_runner.py
EXIT=1
```

All tests outside those five platform-local cases passed in explicit subsets:

```text
71 passed
1 passed, 1 deselected
6 passed, 1 deselected
12 passed, 3 deselected
EXIT=0 (each command)
```

The pull request must use Linux required checks to resolve the Windows-only
residual without changing or skipping repository tests in source.

## Core no-drift object comparison

```text
docs/SUBJECTIVITY_EVIDENCE_PROTOCOL.md
  BASE=7a94b916b45370de98e99d21af1881483ee948a0
  CORE=7a94b916b45370de98e99d21af1881483ee948a0
docs/CURRENT_STATE.md
  BASE=6d639091410ea3fc1a1b17075c02aaf43bbe3634
  CORE=6d639091410ea3fc1a1b17075c02aaf43bbe3634
research-labs/triadic-state-dynamics_v0.1.0
  BASE=b2260664f579dc7fc57686c4ea633344e1e0d54e
  CORE=b2260664f579dc7fc57686c4ea633344e1e0d54e
research-labs/bounded-autonomous-research-loop_v0.1.0
  BASE=4ff2280486ec9fcaf1b45b00200d4138221e38cf
  CORE=4ff2280486ec9fcaf1b45b00200d4138221e38cf
components/aion_astra_autonomous_research_v0.1.0
  BASE=4939e60e3fc5398c6914221731b89fa3df79d097
  CORE=4939e60e3fc5398c6914221731b89fa3df79d097
```

## Patch and rollback

Patch command:

```powershell
git diff --unified=0 --binary --no-ext-diff bb3e5e092c11a1b582a163422611308aaeab1f01 0199d3edb506cc0b85afca45880ba43df3481a43 > qa/zi-wei-dou-shu-v0.1/ZI_WEI_DOU_SHU_V0_1.patch
git apply --unidiff-zero --reverse --check qa/zi-wei-dou-shu-v0.1/ZI_WEI_DOU_SHU_V0_1.patch
```

```text
PATCH_BYTES=409014
PATCH_SHA256=8a08a3e8e9dce8497821605d6c0530b315d91c8df1edf1bc02a4cc8fc358dfd9
PATCH_REVERSE_CHECK_EXIT=0
```

Forward replay used an isolated temporary Git index initialized from the base,
applied the patch, and compared the resulting tree to the core commit:

```text
PATCH_FORWARD_INDEX_APPLY_EXIT=0
PATCH_REPLAY_TREE=c1d2ac8de089323c893d88fd8a04d5b597efa843
CORE_TREE=c1d2ac8de089323c893d88fd8a04d5b597efa843
PATCH_REPLAY_TREE_MATCH=True
```

The source checkout contract was also reopened:

```text
examples/zi-wei-dou-shu_v0.1.0/sources/reviewed-snapshots/wikisource-zi-wei-dou-shu-quan-shu-rev850734.html: text: set
examples/zi-wei-dou-shu_v0.1.0/sources/reviewed-snapshots/wikisource-zi-wei-dou-shu-quan-shu-rev850734.html: eol: lf
```

Rollback command (default dry-run):

```powershell
powershell -ExecutionPolicy Bypass -File scripts/rollback_zi_wei_dou_shu_v0_1.ps1
```

Literal output and status:

```text
ROLLBACK_VERIFY=PASS base=bb3e5e092c11a1b582a163422611308aaeab1f01 core=0199d3edb506cc0b85afca45880ba43df3481a43 patch_sha256=8a08a3e8e9dce8497821605d6c0530b315d91c8df1edf1bc02a4cc8fc358dfd9
ROLLBACK_MODE=DRY_RUN
ROLLBACK_COMMAND=powershell -ExecutionPolicy Bypass -File "<REPOSITORY_ROOT>\scripts\rollback_zi_wei_dou_shu_v0_1.ps1" -Apply
ROLLBACK_EXIT=0
```
