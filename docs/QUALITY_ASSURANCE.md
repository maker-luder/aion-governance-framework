# Quality Assurance

The project uses IQC, IPQC, QC and QA concepts together with status locks, manifests, SHA-256, rollback, NCR and CAPA.

## Evidence rules

- A test is `PASS` only when execution evidence exists.
- A skipped or blocked test is not rewritten as passed.
- Creator-side revalidation is not independent IV&V.
- Historical package evidence and current repository reconstruction evidence are kept separate.
- Changes to code, test fixtures, dependencies or public claims may invalidate prior evidence.

## Public release checks

The release verifier checks manifest integrity, prohibited files, private paths, basic secret patterns, status consistency and required documentation. These scans reduce risk; they do not prove the absence of every possible issue.
