# Contract Architecture

A Contract is a machine-readable set of input/output constraints. Provider-native schemas are never discarded; they are stored as immutable provenance snapshots. Compatibility checks transport, semantic type, schema, cardinality, required metadata, dimensions/duration, language and size limits, not only MIME. Errors use a fixed taxonomy with code, message, retryable, stage and details.

**RU:** Контракт — машиночитаемый набор ограничений входа/выхода. Родные схемы провайдеров не отбрасываются, а хранятся как неизменяемые снимки провенанса. Совместимость проверяет транспорт, семантический тип, схему, кардинальность, обязательные метаданные, размеры/длительность, язык и лимиты размера, а не только MIME. Ошибки — фиксированная таксономия с code, message, retryable, stage, details.

## Key Facts

- **Canonical input port**: name, required, semantic_type, transport_type, schema, constraints, examples, sensitive, artifact_type
- **Error taxonomy**: INVALID_INPUT, CONTRACT_MISMATCH, AUTH_REQUIRED, AUTH_FAILED, POLICY_DENIED, RATE_LIMITED, QUOTA_EXCEEDED, PROVIDER_UNAVAILABLE, PROVIDER_TIMEOUT, SCHEMA_DRIFT, ARTIFACT_TOO_LARGE, ARTIFACT_UNSAFE, EXECUTION_CANCELLED, EXECUTION_FAILED, INTERNAL_ERROR

## Table

| Check | Dimension |
|---|---|
| Transport | HTTP, MCP, A2A, SDK, ... |
| Semantic type | image, text, audio, ... |
| Schema | JSON Schema |
| Cardinality | single vs multiple |
| Metadata | language, dimensions, duration |
| Size limits | max bytes |

## Sources

- docs/SPECS.md §4
- contracts/capability-contract.yaml
