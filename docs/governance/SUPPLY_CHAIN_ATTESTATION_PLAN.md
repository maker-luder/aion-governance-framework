# Supply-Chain Attestation and SBOM Plan

Status: `PREPARATION_ONLY`

This plan prepares the public repository for stronger build provenance and dependency transparency. It does not claim a SLSA level, SPDX conformance, license compatibility, or that attestations currently exist.

## Goals

- bind release artifacts to source commit and workflow identity;
- record artifact digests and build inputs;
- produce a machine-readable dependency inventory / SBOM candidate;
- preserve dependency and license review status separately from build integrity;
- make release verification reproducible by third parties where practical.

## Preferred future flow

`source commit -> CI build -> artifact digest -> SBOM -> signed build provenance / attestation -> verification instructions -> release evidence index`

## Evidence fields

A future release evidence record SHOULD capture:

- repository and source commit SHA;
- workflow file and workflow run identifier;
- runner / build environment summary;
- dependency lock or resolved dependency inventory;
- produced artifact name and SHA-256 digest;
- SBOM format/version and digest;
- attestation format / issuer / subject digest;
- verification command or procedure;
- license review status;
- test evidence references;
- canonical/release approval reference.

## SLSA influence

SLSA provenance is used as methodological guidance for recording **where, when and how** an artifact was produced. The project must not claim a SLSA Build level until the complete requirements for the claimed level and build platform have been checked.

## GitHub artifact attestations

GitHub artifact attestations are a candidate mechanism for cryptographically binding build outputs to GitHub Actions provenance. Enabling them requires a dedicated workflow design and permissions review. This PR does not add attestation-signing permissions yet.

Reason: the current quality workflow is intentionally read-only (`contents: read`). Expanding workflow permissions is a security-relevant change and should be reviewed separately rather than hidden inside documentation convergence.

## SBOM / SPDX preparation

The project prefers an SPDX-compatible machine-readable inventory for future SBOM work, while preserving these distinctions:

- an SBOM describes components and metadata;
- an SBOM does not prove those components are secure;
- an SPDX identifier does not itself decide license compatibility;
- project-owned Apache-2.0 licensing does not automatically resolve third-party obligations.

The existing dependency/license report remains a separate review input until an automated SBOM pipeline is introduced and validated.

## Minimum release gate before enabling attestations

1. Decide exactly which artifact(s) constitute an official release output.
2. Make build steps deterministic enough to identify the expected subject artifact.
3. Generate and validate a dependency/SBOM artifact.
4. Review workflow permission expansion.
5. Bind tests, scanner results and artifact digest in the release evidence index.
6. Add verification instructions and perform a fresh public verification run.

## Non-claims

Current status remains:

- `ATTESTATION_ENABLED = NO`
- `SBOM_RELEASE_GATE = NOT_IMPLEMENTED`
- `SLSA_LEVEL = NOT_CLAIMED`
- `SPDX_CONFORMANCE = NOT_CLAIMED`
- `THIRD_PARTY_LICENSE_COMPATIBILITY = REVIEW_REQUIRED`

`canonical_effect = NONE`
