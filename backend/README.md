# Knowledge Foundation — backend

Provider-neutral knowledge layer for the Universal AI Capability Platform:
LLM-readable wiki, canonical PostgreSQL/SQLite store, and a derived triple graph.

## Layout

```
backend/
├── src/uaicp/
│   ├── domain/     # enums, provenance + evidence marks
│   ├── db/         # SQLAlchemy models, session, repository, contracts
│   ├── graph/      # triple extraction, query, rebuild
│   ├── wiki/       # deterministic llms.txt / llms-full.txt / pages generator
│   └── api/        # read-only FastAPI knowledge API
├── migrations/     # Alembic (Postgres)
└── tests/          # unit + integration + contract
```

## Run

```bash
# Local (SQLite) — no external services needed
export PYTHONPATH=src
python -m uaicp.seed            # create tables, seed, build graph, write wiki
python -m uaicp.wiki.generate   # regenerate wiki only

# API
uvicorn uaicp.api.main:app --reload
```

## Test

```bash
PYTHONPATH=src python -m pytest -q
PYTHONPATH=src python -m ruff check src tests
PYTHONPATH=src python -m mypy src
```

## Notes

- The graph is a **derived projection** (`kg_entity` + `kg_triple`), not a separate
  graph database (ADR-002). Rebuild with `rebuild_graph`.
- Contracts are **append-only**; a schema change inserts a new version.
- Every claim carries provenance + an evidence mark (MEASURED / REPORTED / INFERRED).
- Provider secrets never reach browser clients; this feature exposes read-only data.