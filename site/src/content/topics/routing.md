# Two-Stage Routing

Routing has two stages that are never merged. Stage A, the Capability Router, selects implementations satisfying the semantic goal and contract. Stage B, the Provider Router, selects the concrete provider/endpoint at runtime. Hard gates run before scoring: policy/legal, compatibility, security/trust, auth, channel, availability, budget. Ranking uses profiles QUALITY_FIRST, BALANCED, CHEAPEST_VALID, LOW_LATENCY, PRIVATE, SELF_HOSTED.

**RU:** Роутинг двухэтапный и этапы не сливаются. Этап A — Capability Router выбирает реализации по семантической цели и контракту. Этап B — Provider Router выбирает конкретного провайдера/эндпоинт в рантайме. До скоринга — жёсткие гейты: policy/legal, совместимость, security/trust, auth, канал, доступность, бюджет. Профили: QUALITY_FIRST, BALANCED, CHEAPEST_VALID, LOW_LATENCY, PRIVATE, SELF_HOSTED.

## Key Facts

- **Hard gates (7)**: policy/legal, compatibility, security/trust, auth, channel, availability, budget
- **Decision record**: candidate set, rejection reasons, selected candidate, profile, policy version, timestamp

## Table

| Profile | Optimizes for |
|---|---|
| QUALITY_FIRST | Empirical quality |
| BALANCED | Balanced quality/cost/latency |
| CHEAPEST_VALID | Cost efficiency |
| LOW_LATENCY | p50/p95 latency |
| PRIVATE | Private/self-hosted |
| SELF_HOSTED | Self-hosted only |

## Sources

- docs/SPECS.md §8
- adr/ADR-003.md
