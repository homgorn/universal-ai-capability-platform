# AGENTS.md

Implement from docs/SPECS.md. Do not redesign architecture during implementation without an ADR.

Mandatory invariants:
- Tool != Capability.
- Resource != Interface.
- Capability Router != Provider Router.
- discovered != executable.
- historical contracts are immutable.
- provider secrets never reach browser.
- all external execution passes policy.
- every behavior has tests.

Before coding: read relevant spec/schema/ADR.
After coding: formatter, linter, typecheck, unit tests, integration/contract tests; report changed files, tests, assumptions, unresolved VERIFY/TODO, security and migration impact.
