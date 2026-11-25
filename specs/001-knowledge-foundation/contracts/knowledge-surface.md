# Contract: Knowledge Surface

**Feature**: 001-knowledge-foundation

The knowledge surface is the LLM-readable representation of the platform.

## Artifacts

| Artifact | Path | Purpose |
|----------|------|---------|
| Index | `wiki/llms.txt` | Answer-first index with links to topic pages |
| Full | `wiki/llms-full.txt` | Concatenation of all topic pages |
| Topics | `wiki/pages/<topic>.md` | Per-topic markdown pages |

## `llms.txt` structure

1. `# <Platform Name>` (H1)
2. A blockquote summary of 40–80 words with exact facts (name, purpose, canonical unit,
   core flow).
3. `## Sections` — a Markdown list of links to topic pages, each with a one-line description.
4. `## Invariants` — the mandatory invariants (Tool != Capability, etc.).
5. `## Evidence` — the evidence-mark legend and VERIFY policy.

## Topic page structure

1. `# <Topic>` (H1)
2. Answer-first paragraph within the first 150–300 characters.
3. Fact tables (`| ... |`) and definition lists for exact values.
4. `Sources` section citing first sources (measured / reported URL+date / inferred).

## Guarantees

- Deterministic: byte-identical output for unchanged inputs (content_hash embedded).
- Bilingual: EN canonical, RU mirrored.
- No fabricated facts: unknown values appear as VERIFY items.

## RU

Поверхность знаний: `llms.txt` (answer-first индекс), `llms-full.txt` (полная сборка),
`wiki/pages/*.md` (темы). Детерминизм, двуязычность, без выдуманных фактов.