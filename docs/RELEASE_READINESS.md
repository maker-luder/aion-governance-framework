# Release Readiness

```text
RELEASE_READY = FALSE
```

This status is intentionally conservative. A Git tag, CI pass, or version label does not itself make the framework release-ready or scientifically validated.

A future governed release review must establish all of the following for the exact candidate head:

- documented supported installation and a verified quickstart;
- current public-interface inventory and schema compatibility policy;
- reproducible examples and provenance/evidence verification;
- current changelog, security, support, and feedback expectations;
- green CI on declared supported Python versions;
- no unresolved critical governance inconsistency;
- no unsupported scientific claim;
- fresh exact-head Human Owner release approval.

```text
CI_PASS != SCIENTIFIC_TRUTH
RELEASE != SCIENTIFIC_VALIDATION
HUMAN_OWNER_APPROVAL != INFERRED_FROM_CI
```

GitHub Discussions, labels, and release creation are optional maintainer actions; their existence is not asserted by this document.
