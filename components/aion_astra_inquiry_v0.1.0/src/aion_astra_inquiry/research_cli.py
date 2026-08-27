from __future__ import annotations

import argparse
import os
from pathlib import Path

from .cli import _resolve_output
from .external import ExternalWebPolicy
from .research_campaign import (
    BoundedAutonomousResearchCampaign,
    research_campaign_to_markdown,
    write_research_campaign_report,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Run bounded AION/Astra autonomous research closure"
    )
    parser.add_argument("--root", default=".", help="repository root")
    parser.add_argument(
        "--question",
        action="append",
        default=[],
        help="seed research question; repeatable",
    )
    parser.add_argument("--max-cycles", type=int, default=2)
    parser.add_argument("--max-questions-per-cycle", type=int, default=2)
    parser.add_argument("--max-rounds", type=int, default=3)
    parser.add_argument("--evidence-limit", type=int, default=4)
    parser.add_argument("--max-harness-runs-per-cycle", type=int, default=2)
    parser.add_argument(
        "--no-harness-execution",
        action="store_true",
        help="disable allowlisted state-level research-lab harness execution",
    )
    parser.add_argument(
        "--repository-ref",
        default=os.environ.get("GITHUB_SHA", "UNSPECIFIED"),
    )
    parser.add_argument(
        "--output",
        default="",
        help="output directory; must be outside repository root",
    )
    parser.add_argument(
        "--external-web",
        action="store_true",
        help="enable the existing governed credential-free HTTPS evidence gateway",
    )
    parser.add_argument("--external-max-queries", type=int, default=12)
    parser.add_argument("--external-results-per-query", type=int, default=2)
    parser.add_argument("--external-timeout-seconds", type=float, default=8.0)
    return parser


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
    campaign = BoundedAutonomousResearchCampaign(
        root,
        max_cycles=args.max_cycles,
        max_questions_per_cycle=args.max_questions_per_cycle,
        max_rounds=args.max_rounds,
        evidence_limit=args.evidence_limit,
        repository_ref=args.repository_ref,
        external_web=args.external_web,
        external_policy=external_policy,
        harness_execution=not args.no_harness_execution,
        max_harness_runs_per_cycle=args.max_harness_runs_per_cycle,
    ).run(tuple(args.question))
    json_path, markdown_path = write_research_campaign_report(campaign, output)
    print(research_campaign_to_markdown(campaign))
    print(f"RESEARCH_REPORT_JSON={json_path}")
    print(f"RESEARCH_REPORT_MARKDOWN={markdown_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
