# Feature Specification: HF Ingestion

**Branch**: `004-hf-ingestion` | **Created**: 2026-11-25 | **Status**: Draft

## User Scenarios & Testing

### US1 - Discover HF resources with bounded crawling (P1)
A maintainer runs discovery over a query; the adapter paginates with bounded concurrency,
backs off on 429, caches by revision and detects changes.

**Acceptance Scenarios**
1. Given 25 results and limit 10 per page, when discovered, then 3 pages are fetched.
2. Given a 429, when retried, then backoff with jitter is applied and bounded.
3. Given a dead-letter error, when it fails, then it is recorded and discovery continues.

### US2 - Store raw snapshot and provenance (P1)
Every discovered resource stores an immutable raw snapshot, source URL, revision, observed_at
and parser version; no execution occurs.

**Acceptance Scenarios**
1. Given a resource, when ingested, then raw snapshot and provenance persist.
2. Given a discovered resource, when queried, then status is DISCOVERED (never ACTIVE).

### US3 - Extract a canonical contract (P2)
Gradio OpenAPI schema and `agents.md` are converted into canonical input/output ports with a
deterministic fingerprint.

**Acceptance Scenarios**
1. Given an OpenAPI schema, when extracted, then canonical ports are produced.
2. Given a changed schema, when fingerprinted, then a new fingerprint is produced.
3. Given an unknown schema shape, when extracted, then status is UNKNOWN and no execution.

### Edge Cases
- Empty result set is valid.
- Malformed JSON goes to dead-letter, not a crash.
- Private network URLs are denied by default (SSRF guard).

## Requirements
- FR-001: adapter MUST paginate with cursor/limit.
- FR-002: adapter MUST use exponential backoff with jitter and bounded retries.
- FR-003: HTTP failures MUST go to a dead-letter queue.
- FR-004: each resource MUST store raw snapshot + provenance.
- FR-005: discovered resources MUST have status DISCOVERED (never executable).
- FR-006: Gradio OpenAPI/agents.md MUST extract canonical ports.
- FR-007: contract fingerprint MUST be deterministic.
- FR-008: private network/SSRF URLs MUST be denied.
- FR-009: source/license unknown MUST be marked VERIFY, not assumed.

## Success Criteria
- SC-001: 100% of ingested resources carry raw snapshot + provenance.
- SC-002: 0 discovered resources are executable.
- SC-003: 0 crashes on malformed upstream data.
- SC-004: fingerprints stable for identical schemas.
- SC-005: 100% of private-network URLs denied.

## Assumptions
- HTTP transport is injected (no live network in tests).
- Reuses `uaicp.validation` ports and fingerprints.

## RU
HF-ingestion: пагинация, backoff, dead-letter, raw snapshot + provenance, извлечение
Gradio OpenAPI/agents.md в канонические порты, deтерминированный fingerprint, SSRF-защита.
Найденный ресурс остаётся DISCOVERED.