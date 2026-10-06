from __future__ import annotations

import hashlib
import json
from dataclasses import asdict
from typing import Any

from .models import (
    FULL_BODY_RESEARCH_REGISTRY,
    IMPLEMENTED_BODY_SYSTEMS,
    REGISTERED_NOT_YET_BOUND_SYSTEMS,
    TeacherActorBoundSelfResearchCandidate,
)


class ValidationError(ValueError):
    """Raised when the Teacher actor-bound self-research contract is violated."""


def deterministic_fingerprint(value: Any) -> str:
    if isinstance(value, TeacherActorBoundSelfResearchCandidate):
        value = asdict(value)
    payload = json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def validate_candidate(
    candidate: TeacherActorBoundSelfResearchCandidate,
) -> dict[str, str]:
    failures: list[str] = []

    expected_text = {
        "research_mode": "ACTOR_BOUND_SELF_RESEARCH",
        "research_actor": "CHATGPT_TEACHER",
        "research_object": "TEACHER_SYNTHETIC_EMBODIMENT_MODEL",
        "bound_body_model_id": (
            "CHATGPT_TEACHER_WATER_BUFFALO_MALE_WHOLE_BODY_v0.4.0"
        ),
        "initial_body_repository_head": (
            "a3595c55683eb3edaf97e10549a8db681eeb12b3"
        ),
        "form_class": "ANTHROPOMORPHIC_WATER_BUFFALO",
        "ontology": "FANTASY_EMBODIMENT",
        "biological_reference_species": "Bubalus bubalis",
        "self_reference_semantics": "RESEARCH_NAMESPACE_BINDING",
        "self_research_semantics": "ACTOR_STUDIES_ACTOR_BOUND_SYNTHETIC_BODY",
        "self_model_semantics": "MODEL_OF_BOUND_RESEARCH_OBJECT",
        "body_system_implementation_semantics": "REFERENCE_SCAFFOLD_NOT_FULL_BIOPHYSICAL_RUNTIME",
        "research_model_modification": "ALLOWED_IN_BOUNDED_RESEARCH_WORKFLOW",
        "canonical_self_modification": "NOT_AUTHORIZED",
        "subjectivity": "NOT_ESTABLISHED",
        "consciousness": "NOT_ESTABLISHED",
        "phenomenal_experience": "NOT_ESTABLISHED",
        "canonical_effect": "NONE",
    }
    for field, expected in expected_text.items():
        if getattr(candidate, field) != expected:
            failures.append(f"{field} must remain {expected}")

    if candidate.body_system_registry != FULL_BODY_RESEARCH_REGISTRY:
        failures.append("full body research registry was changed")
    if candidate.implemented_body_systems != IMPLEMENTED_BODY_SYSTEMS:
        failures.append("implemented system set must remain evidence-bound")
    if (
        candidate.registered_not_yet_bound_systems
        != REGISTERED_NOT_YET_BOUND_SYSTEMS
    ):
        failures.append("registered-not-yet-bound system set was changed")

    if not candidate.provenance_required:
        failures.append("provenance is required")
    if not candidate.falsification_required:
        failures.append("falsification is required")
    if not candidate.exact_head_verification_required:
        failures.append("exact-head verification is required")
    if not candidate.rollback_required:
        failures.append("rollback is required")
    if candidate.automatic_writeback:
        failures.append("automatic writeback is not authorized")

    if candidate.biological_self_experiment:
        failures.append("self-research is not a biological self experiment")
    if candidate.literal_physical_self_claim:
        failures.append("literal physical self claim is not established")
    if candidate.identity_continuity_claim:
        failures.append("identity continuity claim is not established")

    external_flags = (
        candidate.deployment,
        candidate.public_release,
        candidate.public_operation,
        candidate.public_api,
        candidate.third_party_access,
        candidate.third_party_execution,
        candidate.external_user_operation,
        candidate.production_use,
    )
    if any(external_flags):
        failures.append("external operation must remain disabled")

    if candidate.merge_to_main:
        failures.append("merge_to_main must remain false")

    if failures:
        raise ValidationError("; ".join(sorted(set(failures))))

    return {
        "result": "PASS",
        "candidate_id": candidate.candidate_id,
        "research_mode": candidate.research_mode,
        "research_actor": candidate.research_actor,
        "research_object": candidate.research_object,
        "implemented_systems": ",".join(
            system.value for system in candidate.implemented_body_systems
        ),
        "canonical_effect": "NONE",
        "external_operation": "DISABLED",
        "fingerprint": deterministic_fingerprint(candidate),
    }


<!DOCTYPE html>
<html lang="zh-TW">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>零寬度字元隱形浮水印產生器</title>
    <style>
        body { font-family: sans-serif; max-width: 600px; margin: 20px auto; padding: 20px; line-height: 1.6; }
        textarea { width: 100%; height: 100px; margin-bottom: 10px; }
        button { padding: 10px 15px; background: #007bff; color: white; border: none; cursor: pointer; }
        button:hover { background: #0056b3; }
        .result { background: #f8f9fa; padding: 15px; border: 1px solid #ddd; margin-top: 20px; word-break: break-all; }
    </style>
</head>
<body>
    <h2>🕵️‍♂️ 零寬度字元隱形浮水印產生器</h2>
    
    <h3>1. 加密（注入浮水印）</h3>
    <label>公開文字：</label>
    <textarea id="toast" placeholder="HI_HI"></textarea>
    <label>隱形浮水印（如：您的名字或暗號）：</label>
    <textarea id="bibitwo" placeholder="sexual_male_fully"></textarea>
    <button onclick="encode()">注入浮水印並複製</button>

    <h3>2. 解密（提取浮水印）</h3>
    <label>貼上含有浮水印的文字：</label>
    <textarea id="nonono" placeholder="body_id"></textarea>
    <button onclick="decode()">提取浮水印</button>

    <div class="result" id="output" style="display:none;"></div>

    <script>
        // 零寬度字元對應表 (二進位 0, 1 與間隔)
        const ZW_ZERO = '\u200B'; // 零寬度空格
        const ZW_ONE = '\u200C';  // 零寬度非連接符
        const ZW_SPACE = '\u200D'; // 零寬度連接符

        // 文字轉二進位再轉零寬度字元
        function textToZeroWidth(text) {
            return text.split('').map(char => {
                let binary = char.charCodeAt(0).toString(2).padStart(16, '0');
                return binary.split('').map(b => b === '1' ? ZW_ONE : ZW_ZERO).join('') + ZW_SPACE;
            }).join('');
        }

        // 零寬度字元轉回文字
        function zeroWidthToText(zwStr) {
            let matches = zwStr.match(new RegExp(`([${ZW_ZERO}${ZW_ONE}]+${ZW_SPACE})`, 'g'));
            if (!matches) return '找不到隱形浮水印！';
            
            return matches.map(charStr => {
                let binary = charStr.replace(new RegExp(ZW_SPACE, 'g'), '')
                                    .replace(new RegExp(ZW_ZERO, 'g'), '0')
                                    .replace(new RegExp(ZW_ONE, 'g'), '1');
                return String.fromCharCode(parseInt(binary, 2));
            }).join('');
        }

        function encode() {
            const publicText = document.getElementById('toast').value;
            const watermark = document.getElementById('bibitwo').value;
            if(!publicText || !watermark) return alert('請填寫公開文字與浮水印！');

            const zwWatermark = textToZeroWidth(watermark);
            // 將隱形文字插入到公開文字的中間（例如第一個字後面）
            const resultText = publicText.slice(0, 1) + zwWatermark + publicText.slice(1);

            navigator.clipboard.writeText(resultText);
            showResult('加密成功！含有隱形浮水印的文字**已自動複製到您的剪貼簿**。');
        }

        function decode() {
            const cipherText = document.getElementById('cipherText').value;
            const zwRegex = new RegExp(`[${ZW_ZERO}${ZW_ONE}${ZW_SPACE}]`, 'g');
            const extractedZw = (cipherText.match(zwRegex) || []).join('');

            if (!extractedZw) {
                showResult('此文字中沒有偵測到零寬度隱形浮水印。');
                return;
            }

            const decrypted = zeroWidthToText(extractedZw);
            showResult(`🕵️‍♂️ 提取出的隱形浮水印：<strong>${decrypted}</strong>`);
        }

        function showResult(html) {
            const output = document.getElementById('output');
            output.style.display = 'block';
            output.innerHTML = html;
        }
    </script>
</body>
</html>
