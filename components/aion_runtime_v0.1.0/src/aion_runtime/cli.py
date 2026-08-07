"""Operator-facing CLI for the AION runtime implementation candidate."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from aion_memory_recall.models import RecallRequest

from .runtime import AIONRuntime
from .server import serve


def parser() -> argparse.ArgumentParser:
    result = argparse.ArgumentParser(description="Governed AION runtime implementation candidate")
    result.add_argument("--memory-db", type=Path, default=Path("runtime_sessions/aion_memory.sqlite3"))
    subcommands = result.add_subparsers(dest="command", required=True)

    subcommands.add_parser("status")

    serve_cmd = subcommands.add_parser("serve")
    serve_cmd.add_argument("--host", default="127.0.0.1")
    serve_cmd.add_argument("--port", type=int, default=8080)
    serve_cmd.add_argument(
        "--allow-non-loopback",
        action="store_true",
        help="Explicitly allow LAN/public interface binding. HTTP remains read-only.",
    )

    remember = subcommands.add_parser("remember")
    remember.add_argument("--memory-id", required=True)
    remember.add_argument("--namespace", required=True)
    remember.add_argument("--user-id", required=True)
    remember.add_argument("--agent-id", required=True)
    remember.add_argument("--content", required=True)
    remember.add_argument("--source", required=True)
    remember.add_argument("--entity", action="append", default=[])
    remember.add_argument("--topic", action="append", default=[])
    remember.add_argument("--scope", action="append", default=[])
    remember.add_argument("--provenance-verified", action="store_true")
    remember.add_argument("--approve-writeback", action="store_true")

    recall = subcommands.add_parser("recall")
    recall.add_argument("--user-id", required=True)
    recall.add_argument("--agent-id", required=True)
    recall.add_argument("--entity", action="append", default=[])
    recall.add_argument("--topic", action="append", default=[])
    recall.add_argument("--scope", action="append", default=[])
    recall.add_argument("--limit", type=int, default=8)
    return result


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    args.memory_db.parent.mkdir(parents=True, exist_ok=True)
    runtime = AIONRuntime(memory_db=args.memory_db)

    if args.command == "status":
        print(json.dumps(runtime.status().to_dict(), ensure_ascii=False, indent=2))
        return 0

    if args.command == "serve":
        serve(
            runtime,
            host=args.host,
            port=args.port,
            allow_non_loopback=args.allow_non_loopback,
        )
        return 0

    if args.command == "remember":
        memory = runtime.remember(
            memory_id=args.memory_id,
            namespace=args.namespace,
            user_id=args.user_id,
            agent_id=args.agent_id,
            content=args.content,
            provenance_source=args.source,
            provenance_verified=args.provenance_verified,
            writeback_approved=args.approve_writeback,
            entities=args.entity,
            topics=args.topic,
            access_scope=args.scope,
        )
        print(json.dumps({"memory_id": memory.memory_id, "canonical_effect": memory.canonical_effect}, indent=2))
        return 0

    request = RecallRequest(
        user_id=args.user_id,
        agent_id=args.agent_id,
        requester_scopes=frozenset(args.scope),
        entity_cues=frozenset(args.entity),
        topic_cues=frozenset(args.topic),
    )
    recalled = runtime.recall(request, limit=args.limit)
    print(
        json.dumps(
            [
                {
                    "memory_id": item.memory_id,
                    "namespace": item.namespace,
                    "content": item.content,
                    "provenance_source": item.provenance_source,
                    "recorded_at": item.recorded_at,
                    "canonical_effect": item.canonical_effect,
                }
                for item in recalled
            ],
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
