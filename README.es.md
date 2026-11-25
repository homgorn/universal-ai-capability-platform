# Plataforma Universal de Capacidades de IA

La Plataforma Universal de Capacidades de IA es un registro, evaluador, enrutador y motor de ejecución independiente del proveedor para recursos de IA heterogéneos: Spaces y Models de Hugging Face, proveedores de inferencia, servicios REST/OpenAPI, herramientas MCP, agentes A2A y APIs internas. Su unidad canónica es **Capability + Contract (capacidad + contrato)**, no un iframe. La plataforma descubre capacidades, valida contratos legibles por máquina, aplica políticas, enruta en dos etapas, ejecuta de forma duradera y publica una wiki legible por modelos de lenguaje.

🌐 **Idioma / Language:** [Español](README.es.md) · [English](README.md) · [Русский](README.ru.md) · [简体中文](README.zh-CN.md) · [Deutsch](README.de.md)

## Datos clave

| Dato | Valor |
|------|-------|
| Website | https://uacp-site.rvcdax.workers.dev |
| Unidad canónica | Capability + Contract |
| Flujo principal | Discovery → Registry → Contract → Evaluation → Policy → Routing → Execution → Composition → Deployment |
| Fuente de verdad | PostgreSQL (SQLite para desarrollo local) |
| Grafo de conocimiento | Proyección derivada de tripletas (`kg_entity` + `kg_triple`), ADR-002 |
| Superficie LLM | `llms.txt`, `llms-full.txt`, 12 páginas temáticas |
| Entidades de dominio | 18 tablas canónicas |
| Taxonomía de errores | 15 códigos normalizados |
| Verificación | `python scripts/health.py` (ruff + mypy + pytest) |
| Pruebas | 56 superadas |
| Licencia | MIT |

## Qué la diferencia

- **Tool ≠ Capability.** La herramienta es una implementación ejecutable; la capacidad es una función semántica estable. Muchas herramientas pueden satisfacer una capacidad.
- **Resource ≠ Interface.** Un Model puede exponer REST/SDK/MCP; un Space puede exponer UI y API de Gradio.
- **Enrutamiento en dos etapas.** Capability Router (ajuste semántico) nunca se fusiona con Provider Router (endpoint de ejecución).
- **Descubierto ≠ ejecutable.** La promoción de confianza T0–T4 y una decisión de política son obligatorias antes de cualquier llamada externa.
- **Contratos inmutables.** Las versiones históricas solo se añaden; la derivación crea una versión nueva y bloquea el enrutamiento incompatible.
- **Evidencia primero.** Cada afirmación se marca MEASURED / REPORTED (URL + fecha) / INFERRED; lo desconocido se etiqueta VERIFY, nunca se inventa.
- **Sin secretos en el navegador.** Las credenciales del proveedor nunca llegan al cliente; se usa un token de sesión con ámbito limitado.

## Inicio rápido

```bash
cd backend
python -m pip install -e ".[dev]"

# Semilla idempotente: tablas, grafo, wiki
export PYTHONPATH=src          # Windows: $env:PYTHONPATH='src'
python -m uaicp.seed

# Verificación completa
python scripts/health.py

# API
uvicorn uaicp.api.main:app --reload
```

PostgreSQL local: `docker compose up -d db` y configurar `DATABASE_URL` (ver `backend/.env.example`).

## Estructura del repositorio

```text
universal-ai-capability-platform-specs-v1/  paquete de especificaciones original
.specify/                                    Spec Kit: constitución, plantillas, scripts
specs/001-knowledge-foundation/              wiki + almacén + grafo de conocimiento
specs/002-contract-validation/               puertos, compatibilidad, errores, CLI
specs/003-execution-gateway/                 máquina de estados, idempotencia, reintentos
backend/src/uaicp/                           implementación
wiki/                                        base de conocimiento generada para LLM
```

## Documentación

- [Índice de la base de conocimiento LLM](wiki/llms.txt)
- [Base de conocimiento completa](wiki/llms-full.txt)
- [Especificación técnica](universal-ai-capability-platform-specs-v1/universal-ai-capability-platform-specs-v1/docs/SPECS.md)
- [Constitución](.specify/memory/constitution.md)

## Metodología

Construido con [GitHub Spec Kit](https://github.com/github/spec-kit): constitution → specify → plan → tasks → analyze → implement. Cada funcionalidad tiene especificación, plan, tareas y pruebas.

## Licencia

MIT — ver [LICENSE](LICENSE).