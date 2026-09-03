# SPDX-License-Identifier: AGPL-3.0-only
# Copyright 2026 AION Project Owner
import argparse
import json
from pathlib import Path

from .provider import calculate, fetch, verify_cache
from .chart import calculate_chart


def main():
    parser = argparse.ArgumentParser(description="Optional AGPL Swiss provider; no public network service")
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("fetch", "verify", "calculate", "chart"):
        command = sub.add_parser(name)
        command.add_argument("--cache", required=True, type=Path)
        if name == "calculate":
            command.add_argument("--jd-tt", type=float, required=True)
        if name == "chart":
            command.add_argument("--datetime", required=True)
            command.add_argument("--latitude", type=float, required=True)
            command.add_argument("--longitude", type=float, required=True)
    args = parser.parse_args()
    if args.command == "fetch":
        result = fetch(args.cache)
    elif args.command == "verify":
        result = {"status": "PASS", "files": len(verify_cache(args.cache))}
    elif args.command == "chart":
        result = calculate_chart(args.cache, args.datetime, args.latitude, args.longitude)
    else:
        result = calculate(args.cache, args.jd_tt)
    print(json.dumps(result, ensure_ascii=False, indent=2, allow_nan=False))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
