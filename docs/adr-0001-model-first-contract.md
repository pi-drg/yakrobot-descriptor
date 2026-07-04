# ADR 0001 — Model-first contract (Pydantic authoritative, JSON Schema generated)

- **Status:** Accepted (deliberate, reversible)
- **Date:** 2026-07-04

## Context

`yakrobot-descriptor` defines the `RobotDescriptor` contract that flows as JSON from a
robot **producer** (today: [`yakrobot-gateway`](../../yakrobot-gateway)) to a
registration **consumer** (today: [`yakrobot-identity`](../../yakrobot-identity)), and
to any future consumer. The contract exists in two forms:

- a **Pydantic model** (`src/yakrobot_descriptor/models.py`), and
- a **JSON Schema** (`src/yakrobot_descriptor/descriptor.schema.json`).

One of them must be the source of truth. The other is derived.

## Decision

**Model-first.** The Pydantic model is authoritative. The JSON Schema is a generated,
committed artifact produced by `scripts/generate_schema.py`
(`RobotDescriptor.model_json_schema()`), stamped with the contract `$id` /
`x-schema-version`. A drift test (`tests/test_contract.py::test_schema_is_in_sync_with_model`)
fails if the model changes without the schema being regenerated.

## Why

- **Single source, no hand-maintained JSON Schema.** Deriving the schema removes a whole
  class of hand-authoring errors (`anyOf` for optionals, `$defs`, `required`).
- **Producer ergonomics.** The team and the only producer today are Python; the gateway
  already builds *and* validates through the Pydantic model, so producing, validating,
  and schema-generation stay one thing.
- **Consumers are unaffected either way.** No consumer imports Pydantic — they consume
  the committed `descriptor.schema.json`. "Authoritative" only decides *who edits the
  contract and how* (Python vs. plain JSON), not what consumers see.

## Consequences

- Changing the contract means editing Python and regenerating the schema. Someone
  working from a non-Python repo cannot edit the source of truth directly.
- The committed schema is always in sync with the model (enforced by the drift test), so
  downstream consumers can trust `descriptor.schema.json` as-is.

## When to revisit → flip to schema-first

Revisit this decision the moment the contract needs to **evolve from outside Python** —
for example:

- a **TypeScript/Node schema consumer** (or producer) that should be able to change the
  contract, or
- `yakrobot-identity`'s own tooling wanting to own the schema.

**Flipping to schema-first** means: the hand-authored `descriptor.schema.json` becomes
the source of truth, and the Pydantic model becomes a **generated / conformance-tested
binding** (e.g. via `datamodel-code-generator`, or a model plus a test asserting it
conforms to the schema). Because everything downstream already depends only on the
committed schema, **nothing downstream has to change** — only how the model is produced.
