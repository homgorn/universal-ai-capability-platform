# Channels and Widget Runtime

Deployment does not depend on direct iframes. Preferred architecture: Browser → Widget Runtime → scoped session token → Execution API → routers → provider. Provider credentials never reach browser clients. Modes: iframe, Web Component, JS SDK, direct API. Channel classes: embedded UI (Web, Telegram Mini App, Discord Embedded App, Teams tab, LINE LIFF) and bot-native (Telegram, Slack, WhatsApp, Google Chat, GitHub, Linear).

**RU:** Развёртывание не зависит от прямых iframe. Предпочтительная архитектура: Browser → Widget Runtime → scoped session token → Execution API → routers → provider. Учётные данные провайдеров не попадают в браузер. Режимы: iframe, Web Component, JS SDK, direct API. Классы каналов: встроенный UI (Web, Telegram Mini App, Discord Embedded App, Teams tab, LINE LIFF) и бот-нативные (Telegram, Slack, WhatsApp, Google Chat, GitHub, Linear).

## Key Facts

- **Invariant**: provider secrets never reach browser
- **SEO**: pages carry real indexable content; widget is the interactive layer

## Table

| Mode | Use |
|---|---|
| iframe | Embedded widget |
| Web Component | Drop-in element |
| JS SDK | Custom integration |
| direct API | Server-to-server |

## Sources

- docs/SPECS.md §15
