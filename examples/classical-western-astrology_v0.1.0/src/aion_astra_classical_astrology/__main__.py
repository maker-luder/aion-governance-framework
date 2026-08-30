"""Print the deterministic synthetic reference chart."""

from .engine import build_chart
from .fixtures import synthetic_reference_input
from .profiles import hellenistic_medieval_profile
from .serialization import canonical_json


def main() -> int:
    chart = build_chart(
        synthetic_reference_input(),
        hellenistic_medieval_profile(),
        chart_id="SYNTHETIC_CLASSICAL_OUTPUT_001",
    )
    print(canonical_json(chart))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
