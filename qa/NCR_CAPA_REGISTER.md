# NCR / CAPA Register

## NCR-PRC-001 — cross-platform absolute-path validation

- **Observation:** the source-derived Astra Workbench test for a Windows drive path (`C:\\escape.txt`) failed on the Linux reconstruction host because `PurePath` followed host semantics.
- **Risk:** a Windows-form absolute path could be treated as a relative filename on POSIX.
- **Corrective action:** the public reconstruction adds `PureWindowsPath` drive and absolute-path checks.
- **Evidence:** Astra Workbench now reports 89 passed.
- **Canonical effect:** none.

## NCR-PRC-002 — monorepo Runtime test dependency resolution

- **Observation:** the bounded Runtime tests initially could not import the Governance Kernel and Astra Workbench when run directly from the reconstructed monorepo.
- **Corrective action:** the repository test runner supplies explicit local source roots, with no package download or network access.
- **Evidence:** bounded Runtime reports 12 passed.
- **Component source change:** none for this item.
