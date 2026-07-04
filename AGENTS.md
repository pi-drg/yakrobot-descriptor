# AGENTS.md — yakrobot-descriptor

## Project Overview

The shared **`RobotDescriptor` contract** — the single source of truth for the JSON
descriptor that flows from a robot **producer** (sibling repo `yakrobot-gateway`) to a
registration **consumer** (sibling repo `yakrobot-identity`), and to any future
consumer. The contract crosses repo boundaries as **JSON**, validated against a
generated JSON Schema. **No repo imports another repo's types** — producers and
consumers only agree on this schema.

This package is deliberately small. It has no chain code, no MCP/FastAPI code, and no
robot-specific logic — just the contract.

## Repository Structure

```
yakrobot-descriptor/
├── src/yakrobot_descriptor/
│   ├── constants.py           # SCHEMA_ID, SCHEMA_VERSION — no pydantic import
│   ├── schema.py               # load_schema()/schema_path() — stdlib only, no pydantic
│   ├── models.py                # RobotDescriptor, BiddingTerms (Pydantic) — [model] extra
│   ├── descriptor.schema.json  # GENERATED — do not hand-edit, see scripts/generate_schema.py
│   └── __init__.py              # lazy re-exports so importing the package needs no pydantic
├── scripts/
│   └── generate_schema.py      # regenerate descriptor.schema.json from models.py
├── examples/
│   └── tumbller.json           # a valid descriptor — canonical example + test fixture
├── tests/
│   └── test_contract.py        # model <-> schema <-> example all agree
└── docs/
    └── adr-0001-model-first-contract.md  # WHY pydantic is authoritative (read this first)
```

## Key Design Decision — read before touching `models.py` or the schema

**[ADR-0001](docs/adr-0001-model-first-contract.md)** — this contract is *model-first*:
the Pydantic model in `models.py` is authoritative, and `descriptor.schema.json` is a
**generated artifact** (never hand-edit it). A drift test
(`test_schema_is_in_sync_with_model`) fails if you edit the model without regenerating.
The ADR also records the trigger for flipping to *schema-first* (a non-Python/TS-Node
consumer needing to evolve the contract) — read it before assuming this is permanent.

## Pydantic is optional — do not break this split

The base install is **pydantic-free**: it ships the generated schema + a stdlib loader
so a consumer can validate JSON without pulling in a validation framework (see
`yakrobot-identity`, which validates via `jsonschema` and never imports pydantic).

- `[model]` extra → pydantic; for **producers** that build/validate via `RobotDescriptor`.
- `[validate]` extra → `jsonschema`; for **consumers** that only check raw JSON.
- `RobotDescriptor`/`BiddingTerms` are imported **lazily** in `__init__.py`
  (`__getattr__`) specifically so `from yakrobot_descriptor import load_schema` never
  imports pydantic. If you add new pydantic-dependent exports, keep them lazy the same way.

## Common Commands

```bash
uv sync --extra dev                        # pydantic + jsonschema + pytest for local dev

uv run python scripts/generate_schema.py   # after editing models.py — commit both files
uv run pytest                              # model / schema / example must stay in sync
```

## Versioning

`SCHEMA_VERSION` / `SCHEMA_ID` live in `constants.py` (imported by `models.py`, not the
other way — keeps them importable without pydantic). Stamped into the schema's `$id` /
`x-schema-version`. Backward-compatible additions bump the minor; the schema does
**not** set `additionalProperties: false`, so consumers ignore unknown keys and older
consumers keep working against newer producers.

## Development Guidelines

- **Never hand-edit `descriptor.schema.json`.** Edit `models.py`, then run
  `scripts/generate_schema.py`, then run the tests.
- **Keep the base package pydantic-free.** Anything that needs pydantic goes behind the
  `[model]` extra and is imported lazily (see `__init__.py`).
- **`examples/tumbller.json` is a live fixture**, not just documentation — it's asserted
  against both the model and the schema in `tests/test_contract.py`. Keep it valid.
- This package should stay free of chain code, MCP/FastAPI code, and robot-plugin types
  — those belong in `yakrobot-gateway` / `yakrobot-identity`.
- See `docs/` for ADRs recording *why*, not just *what* — add a new ADR for future
  contract-shape decisions rather than only updating code comments.

