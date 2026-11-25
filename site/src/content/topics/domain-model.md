# Domain Model

The domain separates 15 entities so that no single descriptor is overloaded: Provider, Resource, Interface, Operation, Tool, Capability, Contract, Evaluation, Health, Policy, Provenance, Execution, Artifact, Recipe, App, Deployment. Tool is an executable implementation; Capability is a normalized semantic function; Resource type and Interface type are independent.

**RU:** Домен разделяет 15 сущностей, чтобы ни один дескриптор не был перегружен: Provider, Resource, Interface, Operation, Tool, Capability, Contract, Evaluation, Health, Policy, Provenance, Execution, Artifact, Recipe, App, Deployment. Tool — исполняемая реализация; Capability — нормализованная семантическая функция; тип Resource и тип Interface независимы.

## Key Facts

- **Tool != Capability**: many tools can implement one capability
- **Resource != Interface**: a Model may expose REST/SDK/MCP; a Space may expose UI + Gradio API
- **Capability ID format**: <domain>.<function>, e.g. image.background_remove

## Table

| Entity | Meaning |
|---|---|
| Provider | Organization/system exposing resources or execution |
| Resource | MODEL, SPACE, API_SERVICE, MCP_SERVER, AGENT_SERVICE, DATASET, REPOSITORY |
| Interface | HTTP_REST, OPENAPI, GRADIO, MCP, A2A, SDK, EMBED, WEBHOOK, CLI |
| Operation | Callable action, e.g. generate, transcribe, remove_background |
| Tool | Executable implementation of an operation |
| Capability | Stable semantic function, e.g. image.upscale |
| Contract | Machine-readable input/output constraints |

## Sources

- docs/SPECS.md §2
- docs/SPECS.md §3
