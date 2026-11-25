# Quickstart: Knowledge Foundation

**Feature**: 001-knowledge-foundation

A runnable validation guide. Implementation details live in `tasks.md`.

## Prerequisites

- Docker (for Postgres) or a local Postgres 16.
- Python 3.13 + `uv`.
- `make` (optional).

## Setup

```bash
# 1. Start Postgres
docker compose up -d db

# 2. Install backend
cd backend
uv sync

# 3. Run migrations
uv run alembic upgrade head

# 4. Seed the fixture corpus
uv run python -m platform.seed
```

## Validation scenarios

### V1 — LLM surface is answer-first (US1, SC-001)
```bash
head -20 wiki/llms.txt
```
Expect: H1, a 40–80 word blockquote summary with exact facts, then a sections list.

### V2 — Provenance is mandatory (US2/SC-002)
```bash
uv run pytest backend/tests/integration/test_provenance.py -q
```
Expect: rows without provenance are rejected; all stored rows carry full provenance.

### V3 — Tenant isolation (US2/SC-003)
```bash
uv run pytest backend/tests/integration/test_tenant_isolation.py -q
```
Expect: tenant A never sees tenant B rows (app filter + RLS).

### V4 — Contract immutability (US2/SC-004)
```bash
uv run pytest backend/tests/integration/test_contract_immutable.py -q
```
Expect: drift creates a new version; old version unchanged (0 mutations).

### V5 — Triple query (US3/SC-005)
```bash
uv run pytest backend/tests/contract/test_graph_query.py -q
```
Expect: seeded pattern queries return the expected triples with 100% precision.

### V6 — Deterministic regeneration (US5/SC-006)
```bash
uv run python -m platform.wiki.generate
git diff --stat wiki/
```
Expect: no diff on unchanged inputs (byte-identical).

### V7 — VERIFY, not fabricated (US4/SC-007)
```bash
uv run pytest backend/tests/unit/test_verify_gates.py -q
```
Expect: unverifiable values appear as VERIFY items; 0 fabricated facts.

## RU

V1: `llms.txt` answer-first. V2: провенанс обязателен. V3: изоляция тенантов.
V4: неизменяемость контрактов. V5: запрос триплетов. V6: байт-идентичная регенерация.
V7: VERIFY вместо выдумок.