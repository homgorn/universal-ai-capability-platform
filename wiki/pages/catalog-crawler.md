# HF Catalog Crawler (MVP-1)

The first active feature is a bounded, resumable crawler of the public Hugging Face Space catalog. It follows the Link rel="next" cursor, stores a canonical record plus an immutable raw snapshot per Space, updates on SHA change and emits a measured inventory report. A 500-Space live sample measured 2026-11-26 found 334 gradio, 98 static, 64 docker and 5 streamlit Spaces; 89 carry the mcp-server tag; 257 declare a license and 244 do not.

**RU:** Первая активная фича — ограниченный, возобновляемый сборщик публичного каталога HF Spaces. Он следует курсору Link rel="next", хранит каноническую запись и неизменяемый raw snapshot, обновляется по SHA и выдаёт измерённый отчёт. Живая выборка 500 Spaces от 2026-11-26: gradio 334, static 98, docker 64, streamlit 5; mcp-server 89; лицензия указана у 257, отсутствует у 244.

## Key Facts

- **Source**: https://huggingface.co/api/spaces?full=true&expand[]=...
- **Measured at**: 2026-11-26, 500 Spaces, 0 failures
- **Full inventory**: not yet run — VERIFY

## Table

| Metric | Measured value |
|---|---|
| Records | 500 (+1 from an earlier incomplete shape) |
| gradio / static / docker / streamlit | 334 / 98 / 64 / 5 |
| mcp-server tag | 89 |
| license known / unknown | 257 / 244 |
| with models / datasets | 355 / 91 |
| unique sha | 492 |

## Sources

- docs/original-research-2026-10-07.md
- docs/adr/ADR-004-ingestion-first.md

## VERIFY

- Full catalog size and exact API rate limits
