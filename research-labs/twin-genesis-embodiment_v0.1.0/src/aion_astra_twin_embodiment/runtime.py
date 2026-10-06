"""Non-3D twin-genesis runtime candidate.

This module materializes validated AION/Astra embodiment instances as a bounded
runtime record. It does not implement rendering, body sensation, sexual
function, intimate interaction, gender assignment, or subjectivity claims.

中文：本模組只建立經驗證的非 3D 執行紀錄；新增的 species_profile_id
（物種設定檔識別碼）只記錄個別 AION/Astra 的形態設定綁定，不代表活體生理、
主觀身體感、性慾或主體性已被建立。
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Any

from .models import EmbodimentInstance, EmbodimentTemplate, SharedGenesisEvent
from .validation import validate_candidate


@dataclass(frozen=True, slots=True)
class TwinRuntimeState:
    runtime_status: str
    shared_root_id: str
    aion_agent_id: str
    astra_agent_id: str
    aion_embodiment_id: str
    astra_embodiment_id: str
    aion_species_profile_id: str
    astra_species_profile_id: str
    validation: dict[str, str]
    rendering_3d: str = "DEFERRED"
    sexual_function: str = "NOT_IMPLEMENTED"
    intimate_interaction: str = "NOT_AUTHORIZED"
    body_sensation: str = "NOT_ESTABLISHED"
    subjectivity_conclusion: str = "NOT_ESTABLISHED"
    canonical_effect: str = "NONE"

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class TwinGenesisRuntime:
    """Create a non-3D runtime state only after governance validation passes."""

    @staticmethod
    def instantiate(
        event: SharedGenesisEvent,
        template: EmbodimentTemplate,
        aion: EmbodimentInstance,
        astra: EmbodimentInstance,
    ) -> TwinRuntimeState:
        validation = validate_candidate(event, template, aion, astra)
        return TwinRuntimeState(
            runtime_status="IMPLEMENTED_NON_3D_CANDIDATE",
            shared_root_id=event.shared_root_id,
            aion_agent_id=event.aion_agent_id,
            astra_agent_id=event.astra_agent_id,
            aion_embodiment_id=aion.embodiment_id,
            astra_embodiment_id=astra.embodiment_id,
            aion_species_profile_id=aion.species_profile_id,
            astra_species_profile_id=astra.species_profile_id,
            validation=validation,
        )
