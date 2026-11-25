# Composition and Recipes

Recipes are typed DAGs; MVP recipes are acyclic. Node types are capability/operation, transformer and validator. Transformers include PDF→text, image→OCR text, image→URL, audio→transcript, JSON→CSV, resize/crop/format conversion. The planner pipeline is goal → output contract → capability search → candidate paths → transformers → graph validation → policy → cost/latency estimate → execution plan.

**RU:** Рецепты — типизированные DAG; MVP-рецепты ацикличны. Типы узлов: capability/operation, transformer, validator. Трансформеры: PDF→text, image→OCR text, image→URL, audio→transcript, JSON→CSV, resize/crop/смена формата. Пайплайн планировщика: goal → output contract → capability search → candidate paths → transformers → graph validation → policy → cost/latency estimate → execution plan.

## Key Facts

- **MVP planner**: may only instantiate approved capabilities and recipes
- **Recipe validation**: incompatible recipe fails unless a registered transformer exists

## Table

| Node type | Role |
|---|---|
| capability/operation | Calls a capability |
| transformer | Converts between types |
| validator | Checks constraints |

## Sources

- docs/SPECS.md §10
