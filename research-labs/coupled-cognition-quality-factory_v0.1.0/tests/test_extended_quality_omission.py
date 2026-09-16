from __future__ import annotations

import pytest

from aion_coupled_quality import QualityError, Severity
from aion_coupled_quality.extended_quality import (
    DataQualityDisposition,
    DataQualityRecord,
    DataRole,
    ExtendedQualityControls,
)


def data_record() -> DataQualityRecord:
    return DataQualityRecord(
        data_id="DATA-REQUIRED-001",
        role=DataRole.FIXTURE,
        provenance_ref="provenance:data-required",
        exact_source_state_ref="git:data-required",
        selection_rule="synthetic fixture selected before execution",
        completeness_ref="check:complete",
        consistency_ref="check:consistent",
        duplicate_check_ref="check:duplicates",
        representativeness_scope="structural QA only",
        privacy_status="PUBLIC_SAFE",
        license_status="REVIEWED",
        known_limitations=("not an empirical population",),
        contamination_risk=Severity.LOW,
        leakage_risk=Severity.LOW,
        synthetic=True,
        empirical_population=False,
        fitness_for_declared_use=True,
        disposition=DataQualityDisposition.FIT_FOR_DECLARED_USE,
    )


def test_full_qms_cannot_silently_omit_data_quality() -> None:
    with pytest.raises(QualityError, match="data-quality record"):
        ExtendedQualityControls().trace_refs()


def test_full_qms_cannot_silently_omit_supplier_quality() -> None:
    with pytest.raises(QualityError, match="supplier-quality record"):
        ExtendedQualityControls(data_quality=(data_record(),)).trace_refs()
