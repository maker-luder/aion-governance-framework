"""Deterministic tool façade over the existing Astra candidate workspace."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Any

from astra_engineering_workbench.workspace import WorkspaceController

from .errors import PolicyDenied
from .models import Action, Observation, TaskSpec
from .policy import ALLOWED_TOOLS, relative_path


class RuntimeTools:
    def __init__(self, controller: WorkspaceController, task: TaskSpec) -> None:
        self.controller = controller
        self.task = task
        self._read_payloads: dict[str, str] = {}

    def execute(self, action: Action) -> Observation:
        if action.tool not in ALLOWED_TOOLS:
            raise PolicyDenied("tool is not admitted")
        if action.tool == "list_files":
            files = [path for path, _size, _digest in self.controller.index_workspace() if not path.startswith(".astra_meta/")]
            return Observation(action.tool, "PASS", {"files": files, "count": len(files)})
        if action.tool == "read_text":
            path = relative_path(action.arguments.get("path", ""))
            if path not in self.task.input_paths:
                raise PolicyDenied("planner attempted to read a path outside task input_paths")
            raw = self.controller.read_file(path)
            if b"\x00" in raw or len(raw) > 1_000_000:
                raise PolicyDenied("input is binary or exceeds the runtime read limit")
            text = raw.decode("utf-8")
            self._read_payloads[path] = text
            return Observation(action.tool, "PASS", {"path": path, "sha256": hashlib.sha256(raw).hexdigest(), "bytes": len(raw), "text": text})
        if action.tool == "write_candidate":
            path = relative_path(action.arguments.get("path", ""))
            if path != self.task.output_path:
                raise PolicyDenied("planner attempted a non-approved output path")
            content = self._build_summary()
            # Workbench 1.0.0 resolves the parent strictly before its atomic
            # writer creates it.  Create only this already policy-validated
            # candidate directory; the approved controller still performs the
            # actual file write and approval validation.
            target_parent = (self.controller.candidate_root / Path(path)).parent
            target_parent.mkdir(parents=True, exist_ok=True)
            digest = self.controller.create_candidate_file(path, content)
            return Observation(action.tool, "PASS", {"path": path, "sha256": digest, "bytes": len(content.encode("utf-8"))})
        if action.tool == "sha256_candidate":
            path = relative_path(action.arguments.get("path", ""))
            if path != self.task.output_path:
                raise PolicyDenied("hash target is not the approved output")
            target = self.controller.candidate_root / Path(path)
            digest = hashlib.sha256(target.read_bytes()).hexdigest()
            return Observation(action.tool, "PASS", {"path": path, "sha256": digest})
        return Observation("complete", "PASS", {"reason": "admitted workflow acceptance criteria met"})

    def _build_summary(self) -> str:
        sections = [
            "# AION/Astra Candidate Runtime Output",
            "",
            f"- task_id: `{self.task.task_id}`",
            f"- objective: {self.task.objective}",
            "- canonical_effect: `NONE`",
            "- subjectivity_conclusion: `NOT_ESTABLISHED`",
            "- deployment: `FALSE`",
            "",
            "## Input inventory",
        ]
        for path in self.task.input_paths:
            text = self._read_payloads[path]
            digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
            sections.extend(
                [
                    f"### {path}",
                    f"- sha256: `{digest}`",
                    f"- characters: {len(text)}",
                    f"- lines: {len(text.splitlines())}",
                    "",
                    "```text",
                    text[:1200].rstrip(),
                    "```",
                    "",
                ]
            )
        sections.append("This file is a candidate derivative pending Owner review.")
        return "\n".join(sections) + "\n"

    @staticmethod
    def audit_payload(observation: Observation) -> dict[str, Any]:
        """Remove text content before audit persistence."""
        return {key: value for key, value in observation.payload.items() if key != "text"}
