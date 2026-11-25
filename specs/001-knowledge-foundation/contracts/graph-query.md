# Contract: Graph Query

**Feature**: 001-knowledge-foundation

The knowledge graph is queried as `(subject, predicate, object)` triples.

## Query forms

| Form | Meaning | Example |
|------|---------|---------|
| `s ? ?` | all triples from a subject | `?s = tool:123` |
| `? ? o` | all triples into an object | `?o = capability:image.background_remove` |
| `s p ?` | specific predicate from subject | `tool:123 --satisfies--> ?` |
| `? p o` | subjects with predicate to object | `? --satisfies--> capability:image.upscale` |
| `s ? o` | any relation between two entities | `tool:123 ? capability:...` |

## Response shape

```json
{
  "request_id": "uuid",
  "trace_id": "uuid",
  "data": {
    "triples": [
      {
        "subject": {"id": "uuid", "type": "TOOL", "name": "..."},
        "predicate": "satisfies",
        "object": {"id": "uuid", "type": "CAPABILITY", "name": "..."},
        "evidence_mark": "MEASURED",
        "source": "...",
        "observed_at": "2026-11-25T00:00:00Z"
      }
    ]
  }
}
```

## Guarantees

- Tenant filtering is mandatory; cross-tenant triples are never returned.
- Results are deterministic for a fixed `graph_version`.
- `object_literal` is returned when `object` is a literal (no entity).
- Unknown predicate returns an empty set, not an error.

## RU

Формы запросов s??, ? ?o, s p?, ? p o, s?o. Ответ — `{request_id, trace_id, data.triples[]}`.
Обязательная tenant-фильтрация, детерминизм по graph_version, пустой набор для неизвестного
предиката.