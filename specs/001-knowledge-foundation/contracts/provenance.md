# Contract: Provenance and Evidence

**Feature**: 001-knowledge-foundation

Every stored claim carries provenance and an evidence mark.

## Provenance fields (mandatory)

| Field | Type | Required | Notes |
|-------|------|----------|-------|
| `source` | string | yes | Origin system/adapter |
| `source_url` | string | yes for REPORTED | First-source URL |
| `observed_at` | datetime | yes for REPORTED | UTC ISO-8601 |
| `source_revision` | string | no | Revision/SHA |
| `raw_snapshot` | jsonb | yes | Immutable provider-native snapshot |
| `parser_version` | string | yes | Parser version |
| `normalized_version` | string | yes | Normalizer version |

## Evidence marks

| Mark | Meaning | Extra requirement |
|------|---------|-------------------|
| `MEASURED` | Observed directly by the platform | none beyond provenance |
| `REPORTED` | Claimed by an external source | `source_url` + `observed_at` |
| `INFERRED` | Derived/uncertain | surfaced as VERIFY item |

## Rules

- A claim with no provenance is rejected (ORM + DB CHECK).
- `REPORTED` without `source_url`/`observed_at` is rejected.
- `INFERRED` values MUST appear in the wiki's VERIFY list, never as facts.
- Historical provenance is immutable once written.

## RU

Провенанс: source, source_url, observed_at, source_revision, raw_snapshot, parser_version,
normalized_version. Метки: MEASURED / REPORTED (URL+дата) / INFERRED (→ VERIFY). Запись без
провенанса отклоняется. Провенанс неизменяем.