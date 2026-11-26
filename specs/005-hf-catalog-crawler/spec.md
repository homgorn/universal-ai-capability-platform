# Feature Specification: HF Catalog Crawler (MVP-1)

**Branch**: `005-hf-catalog-crawler` | **Created**: 2026-11-26 | **Status**: Draft

## User Scenarios & Testing

### US1 - Exhaustive bounded ingestion (P1)
An operator starts a crawl that walks every public HF Space via cursor pagination, without
loading the whole catalog into memory, and persists a canonical record per Space.

**Acceptance Scenarios**
1. Given a page limit of 100, when a crawl runs, then pages follow `Link: rel="next"`.
2. Given 500 requested items, when complete, then 500 canonical records exist (minus duplicates).
3. Given a crawl interrupted, when restarted, then it resumes from the saved cursor.

### US2 - Incremental updates (P1)
A Space whose `sha` is unchanged is not re-fetched deeply; a changed `sha` produces an updated
record and preserves the previous raw snapshot as provenance.

**Acceptance Scenarios**
1. Given unchanged SHA, when re-crawled, then updated_at changes but raw snapshot is unchanged.
2. Given new SHA, when re-crawled, then a new raw snapshot is stored and a change event emitted.

### US3 - Canonical minimal record (P1)
Each record contains id, author, sdk, tags, likes, trending score, runtime, subdomain, sha,
createdAt, lastModified, license (from cardData), models, datasets and source URL.

### US4 - Rate limits and failures (P2)
429 responses are respected using Retry-After and bounded backoff; malformed payloads go to a
dead-letter queue; the crawl never crashes on a single bad Space.

### US5 - Measured inventory report (P2)
After a crawl the system reports measured counts: total records, SDK distribution, share of
`mcp-server` tags, share with OpenAPI/agents.md candidates, licenses present vs unknown.

## Requirements
- FR-001: crawl MUST use cursor pagination from the `Link` header.
- FR-002: crawl MUST be bounded by `--limit` and resumable via a checkpoint.
- FR-003: each Space MUST be stored with a canonical record and raw snapshot.
- FR-004: SHA MUST drive incremental updates; old snapshots remain immutable.
- FR-005: 429 MUST trigger bounded backoff with Retry-After respected.
- FR-006: failures MUST be dead-lettered; crawl MUST continue.
- FR-007: license MUST be parsed from `cardData`; unknown stays unknown (never assumed).
- FR-008: a run MUST emit a measured inventory report (counts/distributions).
- FR-009: no execution, embedding or cloning of Spaces is performed.

## Success Criteria
- SC-001: 100% of requested items persisted (deduplicated by Space id).
- SC-002: 0 duplicate canonical records.
- SC-003: resume produces 0 re-fetched pages before the checkpoint.
- SC-004: 0 crashes on malformed items; all failures dead-lettered.
- SC-005: measured report matches database counts exactly.

## Assumptions
- Public Hub API without a token; `HF_TOKEN` optional to raise rate limits.
- PostgreSQL in production, SQLite for local/dev; raw snapshots stored as JSON.
- Derived from `docs/original-research-2026-10-07.md` (owner chat, 2026-10-07).

## RU
MVP-1: сбор всех HF Spaces через cursor-пагинацию, канонические записи + raw snapshot,
инкремент по SHA, чекпоинт, respect 429, dead-letter и измерённый отчёт по каталогу. Без
исполнения и клонирования пространств.