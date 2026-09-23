from __future__ import annotations

import importlib.util


def test_convergence_module_exists_for_archive_classification_contract() -> None:
    assert (
        importlib.util.find_spec("aion_astra_twin_embodiment.convergence")
        is not None
    ), "convergence module must exist before archive classifications can be loaded"
