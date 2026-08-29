from __future__ import annotations

import argparse
from pathlib import Path
import tempfile

from .campaign import BoundedAutonomousResearchCampaign
from .evidence import export_evidence_views, write_evidence_views
from .models import CampaignLimits


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description="Run a bounded synthetic AION/Astra autonomous research campaign")
    value.add_argument("--root", default=".")
    value.add_argument("--repository-ref", required=True)
    value.add_argument("--question", action="append", default=[])
    value.add_argument("--max-questions", type=int, default=3)
    value.add_argument("--max-experiments", type=int, default=6)
    value.add_argument("--max-rounds", type=int, default=2)
    value.add_argument("--max-seeds", type=int, default=3)
    value.add_argument("--max-follow-up-depth", type=int, default=1)
    value.add_argument("--max-total-steps", type=int, default=200)
    value.add_argument("--max-evidence-items", type=int, default=20)
    value.add_argument("--external-web", action="store_true", default=False)
    value.add_argument("--external-max-queries", type=int, default=0)
    value.add_argument("--output", default="")
    return value


def resolve_output(root: Path, raw_output: str) -> Path:
    output = Path(raw_output).expanduser().resolve() if raw_output.strip() else Path(
        tempfile.mkdtemp(prefix="aion-astra-autonomous-research-")
    ).resolve()
    repository = root.resolve()
    if output == repository or repository in output.parents:
        raise ValueError("campaign output must remain outside the repository root")
    return output


def main(argv: list[str] | None = None) -> int:
    args = parser().parse_args(argv)
    root = Path(args.root).resolve()
    output = resolve_output(root, args.output)
    limits = CampaignLimits(
        max_questions=args.max_questions,
        max_experiments_per_question=args.max_experiments,
        max_peer_rounds=args.max_rounds,
        max_external_queries=args.external_max_queries,
        max_evidence_items=args.max_evidence_items,
        max_seeds=args.max_seeds,
        max_follow_up_depth=args.max_follow_up_depth,
        max_total_campaign_steps=args.max_total_steps,
    )
    report = BoundedAutonomousResearchCampaign(
        root,
        repository_ref=args.repository_ref,
        limits=limits,
        external_web=args.external_web,
    ).run(tuple(args.question))
    views = export_evidence_views(report, root)
    write_evidence_views(output, views)
    summary = "\n".join(
        (
            "# AION/Astra bounded autonomous research campaign",
            "",
            f"- Campaign: `{report.campaign_id}`",
            f"- Repository ref: `{report.repository_ref}`",
            f"- Iterations: `{len(report.iterations)}`",
            f"- Stop reason: `{report.stop_reason}`",
            f"- Run integrity: `{report.run_integrity.value}`",
            f"- Scientific disposition: `{report.scientific_disposition.value}`",
            "- Canonical effect: `NONE`",
            "- Live model execution: `FALSE`",
            "- Autonomous external write: `NO`",
            "- Autonomous authority escalation: `NO`",
            "- Subjectivity conclusion: `NOT_ESTABLISHED`",
            "- Consciousness conclusion: `NOT_ESTABLISHED`",
            "- Identity continuity conclusion: `NOT_ESTABLISHED`",
            "",
        )
    )
    (output / "campaign.md").write_text(summary, encoding="utf-8")
    print(summary)
    print(f"OUTPUT={output}")
    print(f"CAMPAIGN_FINGERPRINT={report.fingerprint}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
