# Phase 0 Research: Knowledge Foundation

**Feature**: 001-knowledge-foundation | **Date**: 2026-11-25

Each decision records: Decision / Rationale / Alternatives considered.

## D1. Triple storage and indexing in PostgreSQL

**Decision**: Store the knowledge graph as a relational projection with two tables:
`kg_entity` (nodes) and `kg_triple` (edges). `kg_triple` columns: `triple_id`,
`subject_id`, `predicate`, `object_id` (nullable), `object_literal` (nullable, jsonb),
`subject_type`, `object_type`, `tenant_id`, `evidence_mark`, `source`, `source_url`,
`observed_at`, `graph_version`, `created_at`. Exactly one of `object_id` / `object_literal`
is non-null (CHECK). Indexes: `(subject_id)`, `(object_id)`, `(predicate)`,
`(subject_id, predicate)`, `(object_id, predicate)`, and a GIN index on `predicate` for
pattern scans. Tenant filtering via `tenant_id` on every index.

**Rationale**: Pattern queries (`? s ?`, `s ? o`, `? ? o`) map to btree/GIN scans; a
derived projection keeps ADR-002 intact and is rebuildable. Measured query complexity can
later justify a graph DB via a new ADR.

**Alternatives**: Neo4j now (rejected: violates ADR-002, adds ops burden); recursive CTEs
over an adjacency table (rejected: slower for multi-hop, harder to index); storing triples
as JSONB rows (rejected: poor queryability).

## D2. Deterministic wiki serialization

**Decision**: Render from the store with Jinja2 templates. Serialize all dynamic values with
`json.dumps(..., sort_keys=True, ensure_ascii=False)`, normalize datetimes to UTC ISO-8601
with `Z`, and order list sections by stable keys (entity id, then name). The output embeds a
`content_hash` (sha256 of the normalized data) instead of a wall-clock timestamp, so
unchanged inputs yield byte-identical files.

**Rationale**: SC-006 requires byte-identical regeneration; wall-clock timestamps would
break diffing.

**Alternatives**: embed generation time (rejected: non-deterministic); no hash (rejected:
no staleness detection).

## D3. Evidence-mark enforcement

**Decision**: `evidence_mark` is a Postgres enum (`MEASURED`, `REPORTED`, `INFERRED`) and is
`NOT NULL` on every claim-bearing table. `REPORTED` requires `source_url` and `observed_at`
(CHECK). A claim with no provenance is rejected at the ORM boundary and by a DB CHECK.
Unverifiable values are stored with `evidence_mark = INFERRED` and surfaced as VERIFY items.

**Rationale**: FR-008/FR-009 and SC-002/SC-007 require zero fabricated facts and full
provenance.

**Alternatives**: app-only validation (rejected: DB is the last line of defense); free-text
mark (rejected: not queryable).

## D4. Tenant isolation

**Decision**: Every tenant-scoped table has `tenant_id` and a composite index leading with
`tenant_id`. Postgres Row-Level Security (RLS) policies restrict rows to the session's
`app.tenant_id` setting, in addition to application-level filtering. The knowledge surface
(wiki) is generated per-tenant or for the public tenant only.

**Rationale**: SC-003 requires zero cross-tenant leaks; RLS is defense-in-depth.

**Alternatives**: app-only filtering (rejected: single missed WHERE leaks); separate
schemas per tenant (rejected: migration overhead at this scale).

## D5. Immutable contract versions

**Decision**: `contract_version` is append-only. The DB role used by the app has `INSERT`
and `SELECT` but not `UPDATE`/`DELETE` on contract tables. A schema change inserts a new
version with an incremented `version` and a `supersedes_id`; the old row is never mutated.

**Rationale**: FR-004 and SC-004 require zero mutations; grants enforce it structurally.

**Alternatives**: soft-delete + update (rejected: mutates history); event-sourced log only
(rejected: harder to query current contract).

## D6. Wiki format (llms.txt / llms-full.txt / markdown)

**Decision**: `llms.txt` follows the answer-first convention: an H1, a one-paragraph
blockquote summary (40–80 words, exact facts), then a Markdown section list with links to
topic pages. `llms-full.txt` concatenates the full topic pages. Topic pages are markdown
with an answer-first paragraph, fact tables, and definition lists. Bilingual: EN canonical,
RU mirrored.

**Rationale**: FR-001/FR-002 and SC-001; matches the owner's AI-ranking rules
(answer-first, information density, tables, trust citations).

**Alternatives**: prose-only docs (rejected: not cited well); JSON only (rejected: not
human/LLM readable prose).

## D7. Test infrastructure

**Decision**: Use `testcontainers` to spin a disposable Postgres for integration and
contract tests; unit tests use in-memory fakes. A `docker-compose.yml` provides a local
Postgres for dev.

**Rationale**: Reproducible CI; no shared-state flakiness.

**Alternatives**: SQLite for tests (rejected: RLS/JSONB/enum semantics differ); shared dev
DB (rejected: isolation risk).

## RU — Резюме research

D1: триплеты — реляционная проекция `kg_entity`+`kg_triple` с btree/GIN индексами и
tenant-фильтром. D2: детерминизм через sort_keys, UTC ISO, content_hash вместо времени.
D3: evidence_mark — enum NOT NULL, REPORTED требует URL+дату, VERIFY для INFERRED.
D4: RLS + app-фильтрация по tenant_id. D5: контракты append-only, права без UPDATE/DELETE.
D6: llms.txt answer-first + llms-full + markdown, двуязычно. D7: testcontainers + Postgres
в docker-compose.