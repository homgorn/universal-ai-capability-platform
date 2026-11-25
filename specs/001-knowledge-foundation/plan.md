# Implementation Plan: Knowledge Foundation

**Branch**: `001-knowledge-foundation` | **Date**: 2026-11-25 | **Spec**: [spec.md](./spec.md)

**Input**: Feature specification from `/specs/001-knowledge-foundation/spec.md`

## Summary

Build the knowledge foundation of the Universal AI Capability Platform: an LLM-readable,
answer-first, fact-dense wiki (`llms.txt` + `llms-full.txt` + markdown), a canonical
PostgreSQL-backed store for all domain entities with tenant isolation, immutable contracts
and provenance, and a derived knowledge graph of `(subject, predicate, object)` triples.
The graph is a relational projection, not a new datastore, per ADR-002.

## Technical Context

**Language/Version**: Python 3.13

**Primary Dependencies**: FastAPI, SQLAlchemy 2.0, Alembic, Pydantic v2, psycopg 3,
pytest, pytest-asyncio, httpx, PyYAML, Jinja2 (wiki rendering)

**Storage**: PostgreSQL 16 (canonical source of truth); object storage is out of scope for
this feature (artifacts referenced by URI only)

**Testing**: pytest (unit + integration + contract), testcontainers or a disposable Postgres
for integration

**Target Platform**: Linux server (containerized); local Windows dev via Docker

**Project Type**: web-service (backend) + documentation generator

**Performance Goals**: triple/pattern queries under 100 ms on a seeded fixture; wiki
regeneration under 5 s for the initial corpus

**Constraints**: tenant isolation enforced on every query; immutable contract versions;
no provider secrets in any client-facing surface; deterministic wiki output

**Scale/Scope**: initial corpus of the platform's own entities (dozens), designed to grow to
thousands of capabilities/tools

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| Principle | Status | Notes |
|-----------|--------|-------|
| I. Provider Neutrality | PASS | Domain entities are provider-neutral; HF is an adapter only |
| II. Contracts Immutable/Versioned | PASS | Contract versions immutable; provenance mandatory |
| III. Discovered != Executable | PASS | No execution in this feature; documented guarantee |
| IV. Evidence & Provenance First | PASS | Evidence mark + VERIFY gates are first-class requirements |
| V. Test-Backed Behavior | PASS | Tests required per story; AT-01…AT-10 referenced |
| VI. Simplicity and YAGNI | PASS | PostgreSQL only; graph is a derived projection (no graph DB) |
| VII. LLM-Readable, Evidence-Dense | PASS | llms.txt + llms-full.txt + answer-first markdown, bilingual |

No violations. No Complexity Tracking entries required.

## Project Structure

### Documentation (this feature)

```text
specs/001-knowledge-foundation/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output
│   ├── knowledge-surface.md
│   ├── graph-query.md
│   └── provenance.md
└── tasks.md             # Phase 2 output (/speckit.tasks)
```

### Source Code (repository root)

```text
backend/
├── src/platform/
│   ├── domain/          # entities, enums, value objects
│   ├── db/              # SQLAlchemy models, session, base
│   ├── graph/           # triple extraction + query
│   ├── wiki/            # deterministic generator (llms.txt, llms-full.txt, md)
│   ├── api/             # FastAPI routers (read-only knowledge API)
│   └── main.py
├── migrations/          # Alembic
├── tests/
│   ├── unit/
│   ├── integration/
│   └── contract/
└── pyproject.toml

wiki/                    # generated artifacts (committed)
├── llms.txt
├── llms-full.txt
└── pages/               # markdown topic pages
```

**Structure Decision**: Single backend project (Python) plus a generated `wiki/` output
directory. The Next.js widget is deferred to a later feature; the structure leaves room for
`frontend/` without introducing it now.

## Phases

- **Phase 0 (Research)**: resolve unknowns (Postgres triple indexing strategy, deterministic
  serialization, evidence-mark enforcement) → `research.md`.
- **Phase 1 (Design)**: `data-model.md`, `contracts/`, `quickstart.md`.
- **Phase 2 (Tasks)**: `/speckit.tasks` → `tasks.md`.
- **Phase 3 (Implement)**: `/speckit.implement`.

## RU — Резюме плана

Стек: Python 3.13, FastAPI, SQLAlchemy 2.0 + Alembic, PostgreSQL 16, Pydantic v2, pytest.
Структура: `backend/src/platform/{domain,db,graph,wiki,api}` + `backend/migrations` +
`backend/tests` + генерируемый каталог `wiki/`. Граф — производная проекция триплетов в
PostgreSQL (без отдельной граф-БД, по ADR-002). Constitution Check — PASS по всем 7 принципам,
нарушений нет. Виджет Next.js отложен на следующую фичу.