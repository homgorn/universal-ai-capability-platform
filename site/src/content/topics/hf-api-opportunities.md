# HF API opportunities

Beyond the catalog endpoint, the owner's token can use HF semantic space search (/api/spaces/semantic-search with ai_category and semanticRelevancyScore), Gradio agents.md and /gradio_api/info for contracts, /gradio_api/mcp/schema for MCP tools, Inference Providers with provider=auto failover, webhooks for Space changes, collections for curated catalogs, and scheduled Jobs for evaluation. Hub rate limits are 500 anonymous / 1000 free / 2500 PRO requests per 5 minutes (reported).

**RU:** Кроме каталога, токен даёт семантический поиск Space-ов, agents.md и /gradio_api/info для контрактов, /gradio_api/mcp/schema для MCP, Inference Providers с failover, webhooks для изменений, collections и Jobs для оценок. Лимиты Hub: 500/1000/2500 запросов за 5 минут (сообщено).

## Key Facts

- **Contract source of truth**: agents.md per Space; openapi.json may return HTML
- **Execution**: Inference Providers router.huggingface.co with provider=auto
- **Legal**: cardData.license must be checked; public ≠ redistribution rights

## Table

| Capability | Endpoint |
|---|---|
| Semantic discovery | /api/spaces/semantic-search?q=... |
| Agent contract | /spaces/{id}/agents.md |
| MCP tools | /gradio_api/mcp/schema |
| Curated catalog | /api/collections?owner=... |
| Change feed | /api/settings/webhooks |

## Sources

- https://huggingface.co/.well-known/openapi.md
- https://huggingface.co/docs/hub/en/rate-limits

## VERIFY

- Token-scoped live calls to semantic search, webhooks and Jobs
