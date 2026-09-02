# SPDX-License-Identifier: AGPL-3.0-only
# Copyright 2026 AION Project Owner
import argparse
import json
from pathlib import Path

from .provider import calculate, fetch, verify_cache


def main():
    parser = argparse.ArgumentParser(description="Optional AGPL Swiss provider; no public network service")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("fetch", "verify", "calculate"):
        command = sub.add_parser(name)
        command.add_argument("--cache", required=True, type=Path)
        if name == "calculate":
            command.add_argument("--jd-tt", type=float, required=True)
    args = parser.parse_args()
    if args.command == "fetch":
        result = fetch(args.cache)
    elif args.command == "verify":
        result = {"status": "PASS", "files": len(verify_cache(args.cache))}
    else:
        result = calculate(args.cache, args.jd_tt)
    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
