"""Bounded, non-shell local subprocess execution."""

from __future__ import annotations

import hashlib
import json
import os
import subprocess
from pathlib import Path

from .audit import AppendOnlyAudit
from .command_policy import CommandPolicy, sanitized_environment
from .models import CommandRequest, CommandResult


class CommandRunner:
    def __init__(self, candidate_root: Path, audit: AppendOnlyAudit) -> None:
        self.candidate_root = candidate_root
        self.audit = audit
        self.policy = CommandPolicy()

    def run(self, request: CommandRequest, *, occurred_at: str) -> CommandResult:
        argv = self.policy.validate(request, self.candidate_root)
        process = subprocess.Popen(
            argv,
            cwd=request.working_directory,
            env=sanitized_environment(),
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=False,
            shell=False,
            creationflags=(
                subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0
            ),
        )
        timed_out = False
        try:
            stdout_raw, stderr_raw = process.communicate(timeout=request.timeout_seconds)
        except subprocess.TimeoutExpired:
            timed_out = True
            self._terminate_tree(process)
            stdout_raw, stderr_raw = process.communicate()
        limit = request.output_limit_bytes
        truncated = len(stdout_raw) > limit or len(stderr_raw) > limit
        stdout = stdout_raw[:limit].decode("utf-8", errors="replace")
        stderr = stderr_raw[:limit].decode("utf-8", errors="replace")
        payload = {
            "command_id": request.command_id,
            "argv": argv,
            "return_code": process.returncode,
            "stdout": stdout,
            "stderr": stderr,
            "timed_out": timed_out,
            "truncated": truncated,
        }
        result_hash = hashlib.sha256(
            json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
        ).hexdigest()
        status = "TIMEOUT" if timed_out else ("PASS" if process.returncode == 0 else "FAIL")
        self.audit.append(
            occurred_at=occurred_at,
            task_id=request.task_id,
            action="command.completed",
            details={**payload, "result_hash": result_hash, "status": status},
        )
        return CommandResult(
            command_id=request.command_id,
            argv=argv,
            return_code=process.returncode,
            stdout=stdout,
            stderr=stderr,
            timed_out=timed_out,
            truncated=truncated,
            result_hash=result_hash,
            status=status,
        )

    @staticmethod
    def _terminate_tree(process: subprocess.Popen[bytes]) -> None:
        if os.name == "nt":
            subprocess.run(
                ["taskkill", "/PID", str(process.pid), "/T", "/F"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                shell=False,
                check=False,
            )
        else:
            process.kill()
