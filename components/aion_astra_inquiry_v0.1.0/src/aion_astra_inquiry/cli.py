from __future__ import annotations

import argparse
import os
from pathlib import Path
import tempfile

from .automation import AutonomousInquiryCampaign, campaign_to_markdown, write_campaign_report
from .external import ExternalWebPolicy


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Run bounded AION/Astra repository inquiry")
    parser.add_argument("--root", default=".", help="repository root")
    parser.add_argument("--question", action="append", default=[], help="seed research question; repeatable")
    parser.add_argument("--max-questions", type=int, default=3)
    parser.add_argument("--max-rounds", type=int, default=3)
    parser.add_argument("--evidence-limit", type=int, default=4)
    parser.add_argument("--repository-ref", default=os.environ.get("GITHUB_SHA", "UNSPECIFIED"))
    parser.add_argument("--output", default="", help="output directory; must be outside repository root")
    parser.add_argument(
        "--external-web",
        action="store_true",
        help="enable governed credential-free HTTPS search/fetch as untrusted external evidence",
    )
    parser.add_argument("--external-max-queries", type=int, default=12)
    parser.add_argument("--external-results-per-query", type=int, default=2)
    parser.add_argument("--external-timeout-seconds", type=float, default=8.0)
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
    external_policy = (
        ExternalWebPolicy(
            max_queries=args.external_max_queries,
            max_results_per_query=args.external_results_per_query,
            timeout_seconds=args.external_timeout_seconds,
        )
        if args.external_web
        else None
    )
    campaign = AutonomousInquiryCampaign(
        root,
        max_questions=args.max_questions,
        max_rounds=args.max_rounds,
        evidence_limit=args.evidence_limit,
        repository_ref=args.repository_ref,
        external_web=args.external_web,
        external_policy=external_policy,
    ).run(tuple(args.question))
    json_path, markdown_path = write_campaign_report(campaign, output)
    markdown = campaign_to_markdown(campaign)
    print(markdown)
    print(f"REPORT_JSON={json_path}")
    print(f"REPORT_MARKDOWN={markdown_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
