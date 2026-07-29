# data/

Two benchmark datasets, each self-contained with its own README, schema, and provenance record.
Their schemas differ intentionally — see [`../METHODOLOGY.md`](../METHODOLOGY.md) for why.

- [`68-query/`](68-query/README.md) — Curify search relevance over 68 curated gold queries.
- [`326-query/`](326-query/README.md) — Curify search-relevance regression benchmark (production
  baseline vs. a candidate branch) over 326 queries.

Validate both with `python3 ../scripts/validate_data.py` from the repository root.
