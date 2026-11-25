# Universal AI Capability Platform

The Universal AI Capability Platform is a provider-neutral capability registry, evaluator, router, execution runtime and composition layer over heterogeneous AI resources (HF Spaces/Models, inference providers, REST/OpenAPI services, MCP tools, A2A agents, internal services). The canonical unit is Capability + Contract, not an iframe. Core flow: Discovery to Registry to Contract to Evaluation to Policy to Routing to Execution to Composition to Deployment.

**RU:** Универсальная платформа AI-возможностей — провайдер-нейтральный реестр возможностей, оценщик, роутер, runtime исполнения и слой композиции над разнородными AI-ресурсами (HF Spaces/Models, inference-провайдеры, REST/OpenAPI, MCP-инструменты, A2A-агенты, внутренние сервисы). Каноническая единица — Capability + Contract, а не iframe. Поток: Discovery → Registry → Contract → Evaluation → Policy → Routing → Execution → Composition → Deployment.

## Key Facts

- **Canonical unit**: Capability + Contract
- **Product chain**: Tool → Capability → Recipe → App → Channel Deployment → Product
- **First source/adapter**: Hugging Face (never the product boundary)

## Table

| Layer | Responsibility |
|---|---|
| Registry | Provider-neutral capability + contract catalog |
| Evaluation | Quality, reliability, latency, cost, safety evidence |
| Routing | Capability Router then Provider Router |
| Execution | Durable, idempotent, cancellable runtime |
| Composition | Typed DAG recipes + transformers |
| Deployment | Apps to channels/tenants |

## Sources

- docs/SPECS.md §0
- adr/ADR-001.md
