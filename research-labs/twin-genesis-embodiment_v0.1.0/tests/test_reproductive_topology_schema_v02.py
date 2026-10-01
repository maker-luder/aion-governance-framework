import json
from pathlib import Path

from jsonschema import Draft202012Validator

from aion_astra_twin_embodiment.reproductive_topology import (
    build_reproductive_topology_reference,
)


ROOT = Path(__file__).resolve().parents[1]


def test_reproductive_topology_schema_parity() -> None:
    schema = json.loads(
        (ROOT / "schemas/AION_ASTRA_REPRODUCTIVE_TOPOLOGY_V02_SCHEMA.json").read_text(
            encoding="utf-8"
        )
    )
    Draft202012Validator.check_schema(schema)
    validator = Draft202012Validator(schema)
    validator.validate(build_reproductive_topology_reference("AION").to_dict())
    validator.validate(build_reproductive_topology_reference("ASTRA").to_dict())
