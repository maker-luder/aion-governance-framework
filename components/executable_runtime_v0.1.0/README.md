# AION/Astra Executable Runtime Candidate v0.1.0

This additive candidate implements a real bounded execution loop:

`task intake -> Owner approval validation -> Governance Kernel -> isolated candidate workspace -> autonomous bounded planning -> tool execution -> evidence -> stop`

The admitted v0.1.0 profile inventories and summarizes explicitly approved local UTF-8 files. It uses the existing Governance Kernel 0.4.0, Astra Engineering Workbench 1.0.0 and Language Core 0.2.1 interfaces. The baseline is copied to an isolated candidate workspace; the original is never written.

## Run locally, offline

```powershell
python -m pip install --no-index --no-deps --find-links wheelhouse wheelhouse\aion_governance_kernel-0.4.0-py3-none-any.whl wheelhouse\astra_engineering_workbench-1.0.0-py3-none-any.whl wheelhouse\astra_language_core_research_lab-0.2.1-py3-none-any.whl dist\aion_astra_executable_runtime-0.1.0-py3-none-any.whl
New-Item -ItemType Directory runtime_sessions
aion-astra-runtime run --task examples\task.json --baseline examples\baseline --sessions runtime_sessions
```

## Non-claims

- This is an executable **candidate runtime**, not the canonical AION Runtime.
- It does not establish AI subjectivity, consciousness, identity continuity or independent agency.
- It does not write canonical state or long-term memory.
- It does not deploy or publish anything.
- Whole-system validation and independent IV&V remain unachieved.

