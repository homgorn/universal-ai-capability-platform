# MVP Roadmap

Delivery is phased P0–P3. P0: repository discipline, canonical domain, PostgreSQL schema/migrations, HF ingestion, Gradio/OpenAPI extraction, contract validation, evaluator, execution gateway, artifact storage, web widget. P1: capability search/router, health/drift, cost engine, compatibility engine, transformers, recipes, Telegram adapter. P2: Replicate/fal adapters, generic OpenAPI, MCP import/export, A2A, document pipeline, data connectors. P3: constrained planner, multi-tenant product layer, billing, UI synthesis, autonomous discovery.

**RU:** Поставка идёт фазами P0–P3. P0: дисциплина репозитория, канонический домен, схема/миграции PostgreSQL, HF-ingestion, извлечение Gradio/OpenAPI, валидация контрактов, оценщик, execution-шлюз, хранилище артефактов, веб-виджет. P1: поиск/роутер, health/drift, стоимостный движок, движок совместимости, трансформеры, рецепты, Telegram-адаптер. P2: адаптеры Replicate/fal, generic OpenAPI, MCP import/export, A2A, документный пайплайн, дата-коннекторы. P3: ограниченный планировщик, мультитенантный продуктовый слой, биллинг, UI-синтез, автономное обнаружение.

## Key Facts

- **Do NOT build initially**: own LLM, vector DB, graph DB, browser engine, Kubernetes, billing, agent swarm

## Table

| Phase | Theme |
|---|---|
| P0 | Foundation + HF ingestion + execution gateway |
| P1 | Routing + health/drift + cost + recipes |
| P2 | More adapters + MCP/A2A + connectors |
| P3 | Planner + multi-tenant + billing + UI synthesis |

## Sources

- docs/SPECS.md §17
- docs/SPECS.md §18
