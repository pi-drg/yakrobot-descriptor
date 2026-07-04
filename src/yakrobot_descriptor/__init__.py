"""yakrobot-descriptor — the shared RobotDescriptor contract.

The single source of truth for the JSON descriptor that flows from a robot producer
(yakrobot-gateway) to a registration consumer (yakrobot-identity) and any future
consumer. The contract crosses repo boundaries as JSON validated against
``descriptor.schema.json``.

The schema + its loader (``load_schema``/``schema_path``) and the version constants are
pydantic-free — installable via the base package or the ``[validate]`` extra. The
Pydantic models (``RobotDescriptor``/``BiddingTerms``) live behind the ``[model]`` extra
and are imported lazily, so a consumer that only validates JSON never needs pydantic.
"""

from yakrobot_descriptor.constants import SCHEMA_ID, SCHEMA_VERSION
from yakrobot_descriptor.schema import load_schema, schema_path

__all__ = [
    "RobotDescriptor",
    "BiddingTerms",
    "SCHEMA_ID",
    "SCHEMA_VERSION",
    "load_schema",
    "schema_path",
]


def __getattr__(name: str):
    # Lazy so importing the package (e.g. for load_schema) doesn't require pydantic.
    if name in ("RobotDescriptor", "BiddingTerms"):
        from yakrobot_descriptor import models

        return getattr(models, name)
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")
