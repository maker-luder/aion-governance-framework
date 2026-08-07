"""Strict local command allowlist with argument-level validation."""

from __future__ import annotations

import os
import re
from pathlib import Path

from .errors import CommandPolicyError
from .models import CommandRequest

NETWORK_TOOLS = {
    "curl", "wget", "invoke-webrequest", "iwr", "ssh", "scp", "ftp",
    "browser", "docker", "kubectl", "az", "aws", "gcloud",
}
FORBIDDEN_TOKENS = {";", "&&", "||", "|", ">", "<", "`", "\n", "\r"}
SECRET_NAME = re.compile(r"(TOKEN|SECRET|PASSWORD|COOKIE|CREDENTIAL|API_KEY)", re.I)
SAFE_ENV_NAMES = {
    "PATH", "PATHEXT", "SYSTEMROOT", "WINDIR", "TEMP", "TMP",
    "PYTHONUTF8", "PYTHONIOENCODING", "NO_COLOR",
}


def sanitized_environment(source: dict[str, str] | None = None) -> dict[str, str]:
    current = dict(os.environ if source is None else source)
    result = {
        key: value
        for key, value in current.items()
        if key.upper() in SAFE_ENV_NAMES and not SECRET_NAME.search(key)
    }
    result["PYTHONUTF8"] = "1"
    result["PYTHONIOENCODING"] = "utf-8"
    return result


class CommandPolicy:
    """Validate explicit argv; never constructs or accepts a shell command."""

    uses_shell = False

    def validate(self, request: CommandRequest, candidate_root: Path) -> tuple[str, ...]:
        if not request.argv or request.timeout_seconds < 1 or request.output_limit_bytes < 1:
            raise CommandPolicyError("command request is incomplete")
        if any(any(token in arg for token in FORBIDDEN_TOKENS) for arg in request.argv):
            raise CommandPolicyError("shell metacharacters are prohibited")
        executable = Path(request.argv[0]).name.lower()
        if executable.endswith(".exe"):
            executable = executable[:-4]
        if executable in NETWORK_TOOLS:
            raise CommandPolicyError("network and cloud commands are prohibited")
        cwd = Path(request.working_directory).resolve(strict=True)
        try:
            cwd.relative_to(candidate_root.resolve(strict=True))
        except ValueError as exc:
            raise CommandPolicyError("working directory escapes candidate workspace") from exc

        args = request.argv[1:]
        if executable in {"python", "python3", "py"}:
            self._validate_python(args, cwd)
        elif executable in {"pytest", "mypy", "coverage"}:
            self._reject_unsafe_args(args)
        elif executable == "git":
            if not args or args[0] not in {"status", "diff"}:
                raise CommandPolicyError("only read-only git status/diff are allowed")
            self._reject_unsafe_args(args)
        else:
            raise CommandPolicyError(f"command is not allowlisted: {executable}")
        return request.argv

    def _validate_python(self, args: tuple[str, ...], cwd: Path) -> None:
        if not args:
            raise CommandPolicyError("python requires an approved module or local script")
        if args[0] == "-m":
            if len(args) < 2 or args[1] not in {
                "pytest", "mypy", "coverage", "compileall", "build", "pip",
                "json.tool",
            }:
                raise CommandPolicyError("python module is not allowlisted")
            if args[1] == "pip":
                required = {"--no-index", "--no-deps"}
                if "install" not in args or not required.issubset(set(args)):
                    raise CommandPolicyError("pip is limited to offline --no-index --no-deps install")
                if any(item in args for item in {"upload", "publish"}):
                    raise CommandPolicyError("package publication is prohibited")
            self._reject_unsafe_args(args)
            return
        if args[0] in {"-c", "-"}:
            raise CommandPolicyError("inline or stdin Python is prohibited")
        script = (cwd / args[0]).resolve(strict=True)
        try:
            script.relative_to(cwd)
        except ValueError as exc:
            raise CommandPolicyError("script escapes working directory") from exc
        if script.suffix.lower() != ".py":
            raise CommandPolicyError("only local Python scripts are allowed")
        self._reject_unsafe_args(args)

    @staticmethod
    def _reject_unsafe_args(args: tuple[str, ...]) -> None:
        if any(arg.startswith(("\\\\", "//")) for arg in args):
            raise CommandPolicyError("UNC arguments are prohibited")
        if any(arg in {"--publish", "upload", "push"} for arg in args):
            raise CommandPolicyError("publication arguments are prohibited")
