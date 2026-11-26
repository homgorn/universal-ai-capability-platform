# Site architecture for 2026

The site is a catalog interface, not a brochure. It has a faceted /spaces search page, 501 entity pages under /space/{id}/, indexable category/tag/SDK hubs, and machine-readable endpoints (/api/items.json, /api/index.json, /api/stats.json, /api/corpus.jsonl, /.well-known/ai-catalog.json). 627 static pages build in 11s. Filter combinations stay client-side with a self-canonical base URL; only curated single-facet hubs are indexable.

**RU:** Сайт — интерфейс каталога, а не брошюра. Есть facet-поиск /spaces, 501 страница /space/{id}/, индексируемые хабы категорий/тегов/SDK и машиночитаемые эндпоинты (/api/items.json и др.). Собирается 627 страниц за 11 с. Комбинации фильтров остаются client-side с self-canonical, индексируются только хабы.

## Key Facts

- **Search**: text + SDK + category + license + tag facets, URL state, client-side JSON
- **Entity page**: answer-first facts table, visible Q&A, related spaces, no invented capability claims
- **Structured data**: SoftwareApplication, CollectionPage + ItemList, BreadcrumbList; FAQPage retired in 2026
- **llms.txt**: cheap convenience, not a standard; Google ignores it — JSON endpoints are primary

## Table

| Route | Purpose |
|---|---|
| /spaces/ | Faceted search + first 24 server-rendered cards |
| /space/{id}/ | Entity page for each HF Space |
| /categories/, /tags/, /sdk/ | Indexable hub pages with ItemList |
| /api/items.json | Full machine-readable catalog |
| /.well-known/ai-catalog.json | Endpoint discovery |

## Sources

- site/src/pages/
- site/public/api/
- docs/original-research-2026-10-07.md §28

## VERIFY

- Search-engine indexation of the new pages
