# Security and Trust

Trust tiers are T0 metadata only, T1 schema inspection, T2 sandboxed smoke test, T3 controlled production execution, T4 privileged/private connector. A discovered resource is not executable by default. Policy decisions are ALLOW, DENY, REQUIRE_APPROVAL, ALLOW_WITH_LIMITS. Data classes are PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED. Provider secrets never reach browser clients.

**RU:** Уровни доверия: T0 — только метаданные, T1 — инспекция схемы, T2 — sandbox smoke-тест, T3 — контролируемое production-исполнение, T4 — привилегированный/приватный коннектор. Найденный ресурс по умолчанию не исполним. Полис-решения: ALLOW, DENY, REQUIRE_APPROVAL, ALLOW_WITH_LIMITS. Классы данных: PUBLIC, INTERNAL, CONFIDENTIAL, RESTRICTED. Секреты провайдеров никогда не попадают в браузер.

## Key Facts

- **Threats**: SSRF, malicious files, arbitrary code, prompt injection, secret exfiltration, data leakage, runaway cost, malicious MCP tools, compromised dependencies, cross-tenant access
- **Controls**: outbound allowlist, SSRF protection, private-network blocking, secret isolation, short-lived credentials, tenant isolation, file limits, malware scanning, audit log, rate limits, budget limits, human approval

## Table

| Tier | Meaning |
|---|---|
| T0 | Metadata only |
| T1 | Schema inspection |
| T2 | Sandboxed smoke test |
| T3 | Controlled production execution |
| T4 | Privileged/private connector |

## Sources

- docs/SPECS.md §6
