# Feature Specification: Artifact Storage (P0 #9)

**Branch**: `009-artifact-storage` | **Date**: 2026-11-28 | **Status**: Draft

## User Scenarios
### US1 - Store typed artifact metadata + URI (P1)
Binary data is written to a storage backend; the registry stores only metadata (type, mime, size,
hash, storage_uri, classification). Binaries never pass through model context.

### US2 - Local backend now, R2 later (P1)
A `LocalStore` is the default dev backend; an `R2Store` is ready and activated by config once R2
is enabled (ADR-005). The store interface is identical.

### US3 - Integrity and classification (P2)
Every artifact has a sha256 hash verified on read; classification defaults to INTERNAL and can
restrict access.

### Edge cases
- Oversized artifact rejected by max_bytes.
- Hash mismatch on read → ARTIFACT_UNSAFE.
- Unknown backend → clear error, no silent fallback.

## Requirements
- FR-001: store bytes in a backend, metadata in the registry.
- FR-002: sha256 hash computed and verified.
- FR-003: max size enforced.
- FR-004: classification recorded; default INTERNAL.
- FR-005: local + R2 backends behind one interface.
- FR-006: never inline binary in API responses.

## Success Criteria
- SC-001: 100% artifacts have hash + URI + classification.
- SC-002: hash mismatch detected on read.
- SC-003: 0 binaries in registry rows.

## RU
MVP: typed metadata + URI; локальный бэкенд сейчас, R2 готов по ADR-005; бинарники не в БД;
sha256 и классификация.