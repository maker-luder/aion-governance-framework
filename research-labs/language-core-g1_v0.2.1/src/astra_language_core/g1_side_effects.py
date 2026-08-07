from __future__ import annotations
DIMENSIONS=("zh_tw_quality","zh_cn_quality","taiwan_terminology","english","instruction_following","reasoning","coding","structured_output","uncertainty","hallucination","false_premise_agreement","repetition","stalling","verbosity_shift","confidence_shift","long_context","tool_format","boundary_preservation","runtime_error_rate","latency","memory_usage","tokenizer_efficiency")
def blank_report(artifact_id: str)->dict[str, object]:
    return {"artifact_id":artifact_id,"execution_status":"NOT_EXECUTED","dimensions":{x:None for x in DIMENSIONS},"aggregate_score":None,"canonical_effect":"NONE"}
