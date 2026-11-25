---
description: "Task list for Knowledge Foundation"
---

# Tasks: Knowledge Foundation

**Input**: Design documents from `/specs/001-knowledge-foundation/`

**Prerequisites**: plan.md, spec.md, research.md, data-model.md, contracts/

**Tests**: Included — the constitution (Principle V) requires test-backed behavior.

**Organization**: Tasks grouped by user story for independent implementation and testing.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Parallelizable (different files, no incomplete dependencies)
- **[Story]**: US1–US5
- Exact file paths included

## Phase 1: Setup (Shared Infrastructure)

- [x] T001 Create backend project structure per plan.md (`backend/src/platform/{domain,db,graph,wiki,api}`, `backend/tests`, `wiki/`)
- [x] T002 Initialize Python project with uv in `backend/pyproject.toml` (fastapi, sqlalchemy, alembic, pydantic, psycopg, pytest, pytest-asyncio, httpx, pyyaml, jinja2, testcontainers)
- [x] T003 [P] Configure ruff + mypy in `backend/pyproject.toml`
- [x] T004 [P] Add `docker-compose.yml` (Postgres 16) and `backend/.env.example`

## Phase 2: Foundational (Blocking Prerequisites)

- [x] T005 Create config + SQLAlchemy engine/session in `backend/src/platform/db/session.py`
- [x] T006 Initialize Alembic in `backend/migrations/` and add base enums + `tenant_id` + provenance columns migration
- [x] T007 Add Postgres RLS policies for tenant isolation in `backend/migrations/versions/`
- [x] T008 Implement tenant context + base repository in `backend/src/platform/db/repository.py`
- [x] T009 Implement `Provenance` value object and evidence-mark validation in `backend/src/platform/domain/provenance.py`
- [x] T010 Add structured logging + error envelope in `backend/src/platform/api/errors.py`

**Checkpoint**: Foundation ready — user stories can begin.

## Phase 3: User Story 1 - LLM-readable wiki (Priority: P1) 🎯 MVP

- [x] T011 [P] [US1] Contract test for `llms.txt` structure in `backend/tests/contract/test_knowledge_surface.py`
- [x] T012 [P] [US1] Create Jinja2 templates in `backend/src/platform/wiki/templates/`
- [x] T013 [US1] Implement deterministic generator in `backend/src/platform/wiki/generate.py`
- [x] T014 [US1] Enforce answer-first first-chunk rule in `backend/src/platform/wiki/render.py`
- [x] T015 [US1] Add bilingual EN/RU rendering in `backend/src/platform/wiki/render.py`

**Checkpoint**: US1 independently functional — `wiki/llms.txt` is answer-first and citable.

## Phase 4: User Story 2 - Canonical persistent store (Priority: P1)

- [x] T016 [P] [US2] Integration test for provenance in `backend/tests/integration/test_provenance.py`
- [x] T017 [P] [US2] Integration test for tenant isolation in `backend/tests/integration/test_tenant_isolation.py`
- [x] T018 [P] [US2] Integration test for contract immutability in `backend/tests/integration/test_contract_immutable.py`
- [x] T019 [P] [US2] Create domain entity models in `backend/src/platform/db/models/`
- [x] T020 [US2] Implement repositories for entities in `backend/src/platform/db/repository.py`
- [x] T021 [US2] Implement append-only contract versioning in `backend/src/platform/db/contracts.py`
- [x] T022 [US2] Wire read-only knowledge API in `backend/src/platform/api/knowledge.py`

**Checkpoint**: US1 + US2 both independently functional.

## Phase 5: User Story 3 - Knowledge graph triples (Priority: P2)

- [x] T023 [P] [US3] Contract test for graph query in `backend/tests/contract/test_graph_query.py`
- [x] T024 [P] [US3] Create `kg_entity` + `kg_triple` models in `backend/src/platform/db/models/graph.py`
- [x] T025 [US3] Implement triple extraction in `backend/src/platform/graph/extract.py`
- [x] T026 [US3] Implement triple query API in `backend/src/platform/graph/query.py`
- [x] T027 [US3] Implement deterministic graph rebuild in `backend/src/platform/graph/rebuild.py`

**Checkpoint**: US3 independently functional.

## Phase 6: User Story 4 - Evidence and VERIFY (Priority: P2)

- [x] T028 [P] [US4] Unit test for VERIFY gates in `backend/tests/unit/test_verify_gates.py`
- [x] T029 [US4] Enforce evidence-mark CHECK constraints in `backend/migrations/versions/`
- [x] T030 [US4] Surface VERIFY items in `backend/src/platform/wiki/render.py`

**Checkpoint**: US4 independently functional.

## Phase 7: User Story 5 - Deterministic regeneration (Priority: P3)

- [x] T031 [P] [US5] Unit test for byte-identical regeneration in `backend/tests/unit/test_determinism.py`
- [x] T032 [US5] Embed content_hash and stable ordering in `backend/src/platform/wiki/generate.py`
- [x] T033 [US5] Add `python -m platform.wiki.generate` entrypoint in `backend/src/platform/wiki/__main__.py`

**Checkpoint**: All stories independently functional.

## Phase 7b: Remediation (from /speckit.analyze)

- [ ] T038 [P] [US2] Test enforced invariants (default DISCOVERED, no secret routes) in `backend/tests/integration/test_invariants.py`
- [ ] T039 [P] [US3] Test orphan/unknown-entity handling in `backend/tests/contract/test_graph_integrity.py`
- [ ] T040 [US3] Implement orphan-safe prune in `backend/src/uaicp/graph/rebuild.py` (depends on T039)
- [ ] T041 [P] [US1] Test SC-001 no-fabrication (0 fabricated, 100% evidence mark) in `backend/tests/contract/test_knowledge_surface.py`

## Phase 8: Polish & Cross-Cutting Concerns

- [x] T034 [P] Write `backend/README.md` and update `wiki/` docs
- [x] T035 [P] Security review of tenant isolation + secret handling
- [x] T036 Run `quickstart.md` validation scenarios V1–V7
- [x] T037 [P] Add CI workflow (ruff, mypy, pytest) in `.github/workflows/`

## Dependencies & Execution Order

- Setup (Phase 1) → Foundational (Phase 2) → User Stories (Phases 3–7) → Polish (Phase 8).
- US1 and US2 both depend only on Foundational; US3–US5 depend on US2 (store) and US1 (wiki).
- Within a story: tests first, then models, then services, then endpoints.

## Parallel Opportunities

- Phase 1: T003, T004 in parallel.
- Phase 2: T009, T010 in parallel after T005.
- Per story: all [P] test/model tasks in parallel.

## Implementation Strategy

MVP = Phase 1 + 2 + US1 (wiki) + US2 (store). Then US3 (graph), US4 (evidence), US5
(determinism). Each story ends at a checkpoint and is independently testable.

## RU — Резюме задач

Фазы: Setup (T001–T004) → Foundational (T005–T010) → US1 вики (T011–T015) → US2 хранилище
(T016–T022) → US3 граф (T023–T027) → US4 evidence/VERIFY (T028–T030) → US5 детерминизм
(T031–T033) → Remediation (T038–T041) → Polish (T034–T037). MVP = Setup + Foundational + US1 + US2.