from __future__ import annotations

import argparse
from pathlib import Path

from .repository_scan import (
    ScanPolicy,
    render_repository_scan_json,
    render_repository_scan_markdown,
    scan_text_repository,
)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "Scan local repository text files and render machine-visible textual "
            "structure as human-readable evidence."
        )
    )
    parser.add_argument("root", type=Path, nargs="?", default=Path("."))
    parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        dest="output_format",
    )
    parser.add_argument("--output", type=Path)
    parser.add_argument("--max-file-bytes", type=int, default=1_048_576)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    report = scan_text_repository(
        args.root,
        policy=ScanPolicy(max_file_bytes=args.max_file_bytes),
    )
    rendered = (
        render_repository_scan_json(report)
        if args.output_format == "json"
        else render_repository_scan_markdown(report)
    )

    if args.output is None:
        print(rendered, end="")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(rendered, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
