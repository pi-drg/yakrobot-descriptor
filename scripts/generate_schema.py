"""Regenerate ``descriptor.schema.json`` from the Pydantic model.

    uv run python scripts/generate_schema.py   # after editing models.py, commit both

This is *model-first*: the Pydantic model is authoritative and the JSON Schema is a
generated, committed artifact (a drift test keeps them in sync). That's a deliberate,
reversible choice — see ``docs/adr-0001-model-first-contract.md``, which records why and
when to flip to schema-first (e.g. once a TypeScript/Node consumer needs to evolve the
contract from outside Python).
"""

import json
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from yakrobot_descriptor.models import SCHEMA_ID, SCHEMA_VERSION, RobotDescriptor

schema = RobotDescriptor.model_json_schema()
# Stamp the identity/version so consumers can pin the contract.
schema = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "$id": SCHEMA_ID,
    "title": "RobotDescriptor",
    "x-schema-version": SCHEMA_VERSION,
    **schema,
}

out = os.path.join(os.path.dirname(__file__), "..", "src", "yakrobot_descriptor",
                   "descriptor.schema.json")
with open(out, "w") as f:
    json.dump(schema, f, indent=2)
    f.write("\n")

print(f"Wrote {os.path.relpath(out)} (contract v{SCHEMA_VERSION})")
