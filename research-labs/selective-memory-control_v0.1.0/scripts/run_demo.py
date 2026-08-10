from aion_selective_memory import SelectiveMemoryStore

store = SelectiveMemoryStore()
store.add(
    memory_id="v1",
    namespace="teacher",
    domain="project",
    purpose="research",
    content="研究分支使用最大化記憶保存",
    source_ref="synthetic:old-observation",
    approval_ref="write-gate:approved:v1",
    created_at="2026-08-11T00:00:00+00:00",
)
store.revise(
    memory_id="v1",
    new_memory_id="v2",
    content="研究分支測試選擇性記憶與修訂優先",
    source_ref="synthetic:correction",
    approval_ref="write-gate:approved:v2",
    created_at="2026-08-11T00:01:00+00:00",
)
trace = store.retrieve(
    "選擇性記憶 修訂",
    namespace="teacher",
    domain="project",
    purpose="research",
)
print("hits:", [(hit.record.memory_id, round(hit.score, 3), hit.record.source_ref) for hit in trace.hits])
print("blocked:", trace.blocked_ids)
