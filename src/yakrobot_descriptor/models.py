"""The ``RobotDescriptor`` contract — the single source of truth for the descriptor a
robot **producer** (e.g. yakrobot-gateway) writes and an identity/registration
**consumer** (e.g. yakrobot-identity) reads.

It crosses repo boundaries as **JSON**, validated against the generated
``descriptor.schema.json`` — no repo imports another repo's types. Python producers may
import these Pydantic models for convenience; non-Python producers just conform to the
schema. New optional fields are added without a major bump; consumers ignore unknown
keys (the schema does not forbid additional properties), so the format can evolve.
"""

from __future__ import annotations

from pydantic import BaseModel, Field

# Re-exported so ``from yakrobot_descriptor.models import SCHEMA_VERSION`` keeps working;
# the canonical (pydantic-free) home is ``constants``.
from yakrobot_descriptor.constants import SCHEMA_ID, SCHEMA_VERSION  # noqa: F401


class BiddingTerms(BaseModel):
    """Marketplace pricing terms carried on the descriptor (flat, wire-facing subset).

    This is the *contract* subset — the robot-side plugin may track more fields
    internally, but only these cross the boundary.
    """

    min_price_cents: int = Field(ge=0)
    currency: str = "usd"
    accepted_task_types: list[str] = Field(default_factory=list)


class RobotDescriptor(BaseModel):
    """Everything a registration layer needs to register/update an agent.

    Public endpoints arrive already resolved. ``bidding_terms`` is ``None`` to opt out
    of the marketplace.
    """

    name: str
    description: str
    robot_type: str
    fleet_provider: str = ""
    fleet_domain: str = ""
    image: str = ""
    mcp_endpoint: str = ""
    fleet_endpoint: str = ""
    tool_names: list[str] = Field(default_factory=list)
    bidding_terms: BiddingTerms | None = None
