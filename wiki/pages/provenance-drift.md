# Provenance and Drift

Every normalized object stores source, source_url, observed_at, source_revision, raw_snapshot, parser_version and normalized_version. A deterministic schema fingerprint detects drift; on change the platform creates a drift event, preserves the old contract, extracts the new one, classifies compatibility (PATCH_COMPATIBLE, BACKWARD_COMPATIBLE, BREAKING, UNKNOWN) and blocks routing if incompatible or unknown. Historical contracts are immutable.

**RU:** Каждый нормализованный объект хранит source, source_url, observed_at, source_revision, raw_snapshot, parser_version, normalized_version. Детерминированный fingerprint схемы обнаруживает дрейф; при изменении создаётся drift-событие, старый контракт сохраняется, извлекается новый, классифицируется совместимость (PATCH_COMPATIBLE, BACKWARD_COMPATIBLE, BREAKING, UNKNOWN) и роутинг блокируется, если несовместимо или неизвестно. Исторические контракты неизменяемы.

## Key Facts

- **Evidence marks**: MEASURED / REPORTED (URL + date) / INFERRED
- **Unknown values**: become VERIFY items, never fabricated facts

## Table

| Compatibility | Meaning |
|---|---|
| PATCH_COMPATIBLE | Additive, safe |
| BACKWARD_COMPATIBLE | Old inputs still valid |
| BREAKING | Incompatible; block routing |
| UNKNOWN | Treat as unsafe; block routing |

## Sources

- docs/SPECS.md §7
- adr/ADR-002.md
