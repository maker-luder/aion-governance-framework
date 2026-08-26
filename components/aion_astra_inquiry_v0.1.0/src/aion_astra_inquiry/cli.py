from __future__ import annotations

import argparse
import os
from pathlib import Path
import tempfile

from .automation import AutonomousInquiryCampaign, campaign_to_markdown, write_campaign_report


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run bounded AION/Astra repository inquiry")
    parser.add_argument("--root", default=".", help="repository root")
    parser.add_argument("--question", action="append", default=[], help="seed research question; repeatable")
    parser.add_argument("--max-questions", type=int, default=3)
    parser.add_argument("--max-rounds", type=int, default=3)
    parser.add_argument("--evidence-limit", type=int, default=4)
    parser.add_argument("--repository-ref", default=os.environ.get("GITHUB_SHA", "UNSPECIFIED"))
    parser.add_argument("--output", default="", help="output directory; must be outside repository root")
    return parser


def _resolve_output(root: Path, raw_output: str) -> Path:
    if raw_output.strip():
        output = Path(raw_output).expanduser().resolve()
    else:
        output = Path(tempfile.mkdtemp(prefix="aion-astra-inquiry-")).resolve()
    repository_root = root.resolve()
    if output == repository_root or repository_root in output.parents:
        raise ValueError("inquiry output must remain outside the repository root")
    return output


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    root = Path(args.root).resolve()
    output = _resolve_output(root, args.output)
    campaign = AutonomousInquiryCampaign(
        root,
        max_questions=args.max_questions,
        max_rounds=args.max_rounds,
        evidence_limit=args.evidence_limit,
        repository_ref=args.repository_ref,
    ).run(tuple(args.question))
    json_path, markdown_path = write_campaign_report(campaign, output)
    markdown = campaign_to_markdown(campaign)
    print(markdown)
    print(f"REPORT_JSON={json_path}")
    print(f"REPORT_MARKDOWN={markdown_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
