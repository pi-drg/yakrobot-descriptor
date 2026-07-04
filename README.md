# yakrobot-descriptor

The shared **RobotDescriptor contract** — the single source of truth for the JSON
descriptor that flows from a robot **producer** (e.g.
[`yakrobot-gateway`](../yakrobot-gateway)) to a registration **consumer** (e.g.
[`yakrobot-identity`](../yakrobot-identity)), and to any future consumer.

The contract crosses repo boundaries as **JSON**, validated against
[`descriptor.schema.json`](src/yakrobot_descriptor/descriptor.schema.json). **No repo
imports another repo's types** — producers and consumers only agree on this schema.

## What's here

- `models.py` — the authoritative Pydantic `RobotDescriptor` (+ `BiddingTerms`).
- `descriptor.schema.json` — the **generated** JSON Schema. Language-agnostic form of
  the contract; this is what non-Python consumers validate against.
- `scripts/generate_schema.py` — regenerates the schema from the model.
- `examples/tumbller.json` — a valid descriptor.

## How each side uses it

The base install is **pydantic-free** — it ships `descriptor.schema.json` plus a stdlib
loader (`load_schema` / `schema_path`). Pick the extra that matches your role:

- **Python producer** (gateway) → `yakrobot-descriptor[model]`:
  `from yakrobot_descriptor import RobotDescriptor`, build it from local data,
  `model_dump_json()` → write JSON. Pydantic validates.
- **Consumer that wants no Pydantic** (identity's pure-dataclass core) →
  `yakrobot-descriptor[validate]`: validate raw JSON against `load_schema()` with
  `jsonschema`, then map into its own type. Pydantic is never imported.
- **Non-Python consumer** (e.g. a Node identity via `ajv`): validate against
  `descriptor.schema.json` directly.

## Versioning

`SCHEMA_VERSION` (in `models.py`, stamped into the schema `$id` / `x-schema-version`)
is the contract version. Backward-compatible additions bump the minor; the schema does
**not** forbid additional properties, so consumers ignore unknown keys and older
consumers keep working against newer producers. Consumers pin a version.

## Design decisions

- [ADR 0001 — Model-first contract](docs/adr-0001-model-first-contract.md): why Pydantic
  is authoritative and the JSON Schema is generated, and when to flip to schema-first
  (e.g. a TypeScript/Node consumer that needs to evolve the contract from outside Python).

## Consuming it

Depend on a pinned release (reproducible) or a local path (dev), choosing the extra for
your role (`[model]` to produce via Pydantic, `[validate]` to check JSON without it):

```toml
dependencies = ["yakrobot-descriptor[model]>=0.1"]     # producer
# dependencies = ["yakrobot-descriptor[validate]>=0.1"] # consumer, no pydantic

[tool.uv.sources]
# reproducible:
yakrobot-descriptor = { git = "https://…/yakrobot-descriptor", tag = "v0.1.0" }
# or local dev:
# yakrobot-descriptor = { path = "../yakrobot-descriptor", editable = true }
```

## Develop

```bash
uv run python scripts/generate_schema.py   # after editing models.py
uv run pytest                              # model / schema / example stay in sync
```
