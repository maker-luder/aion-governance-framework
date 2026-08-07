from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .admission import AdmissionThresholds, assess_admission, decision_to_dict
from .config import generation_settings, load_json_compatible_yaml
from .dataset import load_prompt_pairs
from .errors import LanguageLabError, ValidationError
from .evaluation import EvaluationRun, evaluate
from .hashing import sha256_file, shard_manifest
from .json_types import JsonValue
from .models import ModelNode
from .registry import ModelRegistry
from .reports import compare_runs, write_json_report, write_markdown_report
from .runtime import MockRuntime, OllamaRuntime


def _path(value: str) -> Path:
    return Path(value)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Offline Astra language-core research lab")
    sub = parser.add_subparsers(dest="command", required=True)
    init = sub.add_parser("init-lab", help="Create a registry from a model configuration")
    init.add_argument("--models", type=_path, required=True)
    init.add_argument("--output", type=_path, required=True)
    register = sub.add_parser("register-model", help="Register one experimental model node")
    register.add_argument("--config", type=_path, required=True)
    register.add_argument("--registry", type=_path, required=True)
    hashing = sub.add_parser("hash-model", help="Hash one file or a deterministic shard set")
    hashing.add_argument("--path", type=_path, required=True)
    dataset = sub.add_parser(
        "validate-dataset", help="Validate paired Traditional/Simplified JSONL"
    )
    dataset.add_argument("--path", type=_path, required=True)
    run = sub.add_parser("run-eval", help="Run a local mock or localhost Ollama evaluation")
    run.add_argument("--config", type=_path, required=True)
    run.add_argument("--dataset", type=_path, required=True)
    run.add_argument("--output", type=_path, required=True)
    compare = sub.add_parser("compare-runs", help="Compare baseline and candidate run records")
    compare.add_argument("--baseline", type=_path, required=True)
    compare.add_argument("--candidate", type=_path, required=True)
    compare.add_argument("--output", type=_path, required=True)
    report = sub.add_parser("build-report", help="Create Markdown from a JSON comparison")
    report.add_argument("--input", type=_path, required=True)
    report.add_argument("--output", type=_path, required=True)
    status = sub.add_parser("qa-status", help="Evaluate conservative QA gates")
    status.add_argument("--model", type=_path, required=True)
    return parser


def _objects(value: JsonValue, label: str) -> list[dict[str, JsonValue]]:
    if not isinstance(value, list) or any(not isinstance(item, dict) for item in value):
        raise ValidationError(f"{label} must be an array of objects")
    return [item for item in value if isinstance(item, dict)]


def execute(args: argparse.Namespace) -> int:
    if args.command == "init-lab":
        data = load_json_compatible_yaml(args.models)
        nodes = [ModelNode.from_dict(item) for item in _objects(data.get("models"), "models")]
        ModelRegistry(args.output).create(nodes)
        print(f"Created registry: {args.output}")
    elif args.command == "register-model":
        node = ModelNode.from_dict(load_json_compatible_yaml(args.config))
        ModelRegistry(args.registry).register(node)
        print(f"Registered {node.model_id} in {args.registry}")
    elif args.command == "hash-model":
        if args.path.is_file():
            print(sha256_file(args.path))
        else:
            print(json.dumps(shard_manifest(args.path, list(args.path.rglob("*.*"))), indent=2))
    elif args.command == "validate-dataset":
        pairs = load_prompt_pairs(args.path)
        print(f"Validated {len(pairs)} prompt pairs: {args.path}")
    elif args.command == "run-eval":
        data = load_json_compatible_yaml(args.config)
        runtime_name = data.get("runtime")
        runtime = MockRuntime({}) if runtime_name == "mock" else OllamaRuntime()
        settings_raw = data.get("settings")
        if not isinstance(settings_raw, dict):
            raise ValidationError("settings must be an object")
        run = EvaluationRun(
            run_id=str(data.get("run_id")),
            model_id=str(data.get("model_id")),
            model_name=str(data.get("model_name")),
            settings=generation_settings(settings_raw),
        )
        evaluate(run, load_prompt_pairs(args.dataset), runtime, args.output)
        print(f"Wrote run artifact: {args.output}")
    elif args.command == "compare-runs":
        write_json_report(compare_runs(args.baseline, args.candidate), args.output)
        print(f"Wrote comparison: {args.output}")
    elif args.command == "build-report":
        value: JsonValue = json.loads(args.input.read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            raise ValidationError("report input must be an object")
        write_markdown_report(value, args.output)
        print(f"Wrote report: {args.output}")
    elif args.command == "qa-status":
        node = ModelNode.from_dict(load_json_compatible_yaml(args.model))
        print(
            json.dumps(
                decision_to_dict(assess_admission(node, {}, AdmissionThresholds())), indent=2
            )
        )
    return 0


def main(argv: list[str] | None = None) -> int:
    try:
        return execute(build_parser().parse_args(argv))
    except (LanguageLabError, OSError, json.JSONDecodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
