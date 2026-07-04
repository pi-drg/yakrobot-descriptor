"""Contract identity + version constants — importable without pydantic.

Kept separate from ``models`` so consumers that only validate JSON against the shipped
schema (e.g. yakrobot-identity) can read the version without pulling the Pydantic model.
"""

# Bump the minor for backward-compatible additions, the major for breaking changes.
SCHEMA_VERSION = "1.0.0"
SCHEMA_ID = "https://yakrobot.org/schemas/robot-descriptor/v1.json"
