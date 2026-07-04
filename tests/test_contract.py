"""Contract tests: the Pydantic model, the generated schema, and the example agree."""

import json
from pathlib import Path

import pytest

from yakrobot_descriptor import RobotDescriptor, load_schema, schema_path

EXAMPLE = Path(__file__).resolve().parent.parent / "examples" / "tumbller.json"


def test_example_parses_into_model():
    d = RobotDescriptor.model_validate_json(EXAMPLE.read_text())
    assert d.name == "Tumbller-Finland-01"
    assert d.bidding_terms is not None
    assert d.bidding_terms.min_price_cents == 50


def test_schema_is_in_sync_with_model():
    # Guards against editing the model without regenerating descriptor.schema.json.
    from yakrobot_descriptor.models import SCHEMA_VERSION

    bundled = load_schema()
    regenerated = RobotDescriptor.model_json_schema()
    assert bundled["properties"].keys() == regenerated["properties"].keys()
    assert bundled["required"] == regenerated["required"]
    assert bundled["x-schema-version"] == SCHEMA_VERSION


def test_example_validates_against_schema():
    jsonschema = pytest.importorskip("jsonschema")
    jsonschema.validate(json.loads(EXAMPLE.read_text()), load_schema())


def test_schema_allows_forward_compatible_extra_keys():
    # Consumers must tolerate unknown keys so producers can add fields without a break.
    jsonschema = pytest.importorskip("jsonschema")
    doc = json.loads(EXAMPLE.read_text())
    doc["future_field"] = "ignored"
    jsonschema.validate(doc, load_schema())


def test_schema_path_points_at_a_file():
    assert Path(schema_path()).is_file()
