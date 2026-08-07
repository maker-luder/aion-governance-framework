"""Change-impact based validation planning."""

from __future__ import annotations

from .enums import ChangeCategory
from .models import EvidenceReference, ValidationPlan


def create_validation_plan(
    category: ChangeCategory,
    evidence: tuple[EvidenceReference, ...] = (),
) -> ValidationPlan:
    reusable = tuple(
        item.evidence_id for item in evidence if item.validity_status.value == "REUSABLE_EVIDENCE"
    )
    invalidated = tuple(
        item.evidence_id for item in evidence if item.evidence_id not in reusable
    )
    mapping = {
        ChangeCategory.DOCUMENT_ONLY: (("document-diff",), (), (), ("links",)),
        ChangeCategory.PACKAGING: (("archive-integrity",), (), ("package",), ("manifest",)),
        ChangeCategory.TEST_ONLY: (("affected-tests",), ("mypy-related",), (), ()),
        ChangeCategory.SOURCE_LOCAL: (
            ("affected-tests", "direct-regression"),
            ("mypy-related",),
            (),
            (),
        ),
        ChangeCategory.SCHEMA: (
            ("schema-tests", "migration-tests"),
            ("mypy-related",),
            (),
            ("persistence",),
        ),
        ChangeCategory.DEPENDENCY: (
            ("full-tests",),
            ("mypy-full",),
            ("wheel", "sdist"),
            ("offline-install",),
        ),
        ChangeCategory.CROSS_COMPONENT_INTERFACE: (
            ("adapter-tests",),
            ("mypy-full",),
            (),
            ("integration",),
        ),
        ChangeCategory.SECURITY_POLICY: (
            ("security-regression", "full-tests"),
            ("mypy-full",),
            (),
            ("integration",),
        ),
        ChangeCategory.RUNTIME_BEHAVIOR: (
            ("full-tests",),
            ("mypy-full",),
            ("wheel", "sdist"),
            ("integration", "offline-install"),
        ),
    }
    tests, static, builds, integration = mapping[category]
    full = (
        "runtime, dependency, or security policy change invalidates broad evidence"
        if category in {
            ChangeCategory.DEPENDENCY,
            ChangeCategory.SECURITY_POLICY,
            ChangeCategory.RUNTIME_BEHAVIOR,
        }
        else None
    )
    return ValidationPlan(
        category, tests, static, builds, integration, reusable, invalidated, full
    )
