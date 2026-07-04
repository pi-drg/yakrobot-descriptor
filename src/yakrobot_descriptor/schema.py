"""Access to the bundled JSON Schema — the language-agnostic form of the contract.

Consumers that don't want a Pydantic dependency (e.g. yakrobot-identity's pure-dataclass
core) can validate raw JSON against this schema with the ``jsonschema`` library instead
of importing the models here.
"""

import json
from functools import lru_cache
from importlib.resources import files

_SCHEMA_FILE = "descriptor.schema.json"


def schema_path() -> str:
    """Filesystem path to the bundled ``descriptor.schema.json``."""
    return str(files("yakrobot_descriptor").joinpath(_SCHEMA_FILE))


@lru_cache(maxsize=1)
def load_schema() -> dict:
    """Return the bundled JSON Schema as a dict."""
    return json.loads(files("yakrobot_descriptor").joinpath(_SCHEMA_FILE).read_text())
