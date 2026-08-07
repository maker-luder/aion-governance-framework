"""Bounded planner implementations for the executable loop."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Protocol

from astra_language_core.models import GenerationSettings
from astra_language_core.runtime import OllamaRuntime

from .errors import PlannerFailure
from .models import Action, Observation, TaskSpec
from .policy import ALLOWED_TOOLS, validate_endpoint


class Planner(Protocol):
    def next_action(self, task: TaskSpec, observations: tuple[Observation, ...]) -> Action:
        """Choose exactly one bounded action."""


class DeterministicInventoryPlanner:
    """Autonomously completes one admitted inventory/summarize workflow."""

    def next_action(self, task: TaskSpec, observations: tuple[Observation, ...]) -> Action:
        if not any(item.tool == "list_files" for item in observations):
            return Action("list_files")
        reads = {
            str(item.payload.get("path"))
            for item in observations
            if item.tool == "read_text" and item.status == "PASS"
        }
        for path in task.input_paths:
            if path not in reads:
                return Action("read_text", {"path": path})
        if not any(item.tool == "write_candidate" for item in observations):
            return Action("write_candidate", {"path": task.output_path})
        if not any(item.tool == "sha256_candidate" for item in observations):
            return Action("sha256_candidate", {"path": task.output_path})
        return Action("complete")


@dataclass(slots=True)
class OllamaJsonPlanner:
    """Optional localhost-only model planner; tool decisions remain policy-validated."""

    model_name: str
    endpoint: str = "http://127.0.0.1:11434"

    def next_action(self, task: TaskSpec, observations: tuple[Observation, ...]) -> Action:
        validate_endpoint(self.endpoint, task.network_policy)
        runtime = OllamaRuntime(self.endpoint, timeout_seconds=30.0)
        compact = [
            {"tool": item.tool, "status": item.status, "keys": sorted(item.payload)}
            for item in observations
        ]
        prompt = json.dumps(
            {
                "instruction": "Return JSON only: {tool, arguments}. Choose one admitted tool.",
                "objective": task.objective,
                "input_paths": task.input_paths,
                "output_path": task.output_path,
                "allowed_tools": sorted(ALLOWED_TOOLS),
                "observations": compact,
            },
            ensure_ascii=False,
        )
        completion = runtime.generate(
            self.model_name,
            prompt,
            GenerationSettings(seed=20260804, temperature=0.0, top_p=1.0, top_k=1, repeat_penalty=1.0, num_ctx=4096, max_output_tokens=256),
        )
        try:
            raw = json.loads(completion.text)
        except json.JSONDecodeError as exc:
            raise PlannerFailure("localhost planner returned invalid JSON") from exc
        if not isinstance(raw, dict) or raw.get("tool") not in ALLOWED_TOOLS:
            raise PlannerFailure("localhost planner selected an unadmitted tool")
        arguments = raw.get("arguments", {})
        if not isinstance(arguments, dict) or not all(isinstance(k, str) and isinstance(v, str) for k, v in arguments.items()):
            raise PlannerFailure("planner arguments must be a string map")
        return Action(str(raw["tool"]), dict(arguments))

