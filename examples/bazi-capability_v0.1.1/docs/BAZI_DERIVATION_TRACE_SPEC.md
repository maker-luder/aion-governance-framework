# Bazi Derivation Trace Specification

Each natal result records source input ID, immutable rule profile ID,
algorithm version, calendar-source version, calculation run ID, ordered
derivation trace, generated time and SHA-256 derivation hash.

Canonical JSON uses sorted keys and normalized immutable records. The hash
detects changed inputs, rule versions or derived facts; it is not a digital
signature, legal attestation or proof of metaphysical truth.
