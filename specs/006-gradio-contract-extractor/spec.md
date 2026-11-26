# Feature Specification: Gradio Contract Extractor (MVP-2)

**Branch**: `006-gradio-contract-extractor` | **Date**: 2026-11-26 | **Status**: Draft

## User Scenarios
### US1 - agents.md as source of truth (P1)
A candidate Space's `agents.md` is parsed into endpoint URLs, upload hints, auth hints and
call/poll mechanics. No provider code is executed.

### US2 - canonical ports from /gradio_api/info (P1)
`named_endpoints` are converted into canonical input/output ports with semantic types and a
deterministic fingerprint.

### US3 - MCP schema detection (P2)
`/gradio_api/mcp/schema` is parsed as a candidate interface; absence is recorded, not assumed.

### Edge cases
- `openapi.json` may return HTML — never treated as schema.
- Missing agents.md or info → candidate stays UNKNOWN, no contract claim.
- Private/ZeroGPU Spaces require token — recorded as auth hint.

## Requirements
- FR-001: parse agents.md endpoints, uploads, auth and poll hints.
- FR-002: convert /gradio_api/info parameters into canonical ports.
- FR-003: prefer semantic types over MIME-only matching.
- FR-004: fingerprint deterministic over canonical JSON.
- FR-005: missing/invalid data → UNKNOWN status, no execution.
- FR-006: MCP schema parsed when present.
- FR-007: all claims carry provenance (source URL + observed_at).

## Success Criteria
- SC-001: 100% of fixture endpoints produce ports.
- SC-002: fingerprints stable across key reorder.
- SC-003: 0 executions of provider code in tests.
- SC-004: missing schema → UNKNOWN, never ACTIVE.

## RU
MVP-2: agents.md как источник истины, /gradio_api/info → канонические порты, MCP schema как
кандидат. Без исполнения; неизвестное остаётся UNKNOWN.