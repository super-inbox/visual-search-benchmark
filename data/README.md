# data/

Two benchmark datasets, each self-contained with its own README, schema, and provenance record.
Their schemas differ intentionally — see [`../METHODOLOGY.md`](../METHODOLOGY.md) for why.

- [`68-query/`](68-query/README.md) — Curify search relevance over 68 curated gold queries, with
  real cross-platform screenshot evidence (Curify/Bing/Google/Canva/Pinterest) for 12 of the 68 —
  browsable at [`68-query/gallery/index.html`](68-query/gallery/index.html).
- [`326-query/`](326-query/README.md) — Curify search-relevance regression benchmark (production
  baseline vs. a candidate branch) over 326 queries, plus real Google Images and Curify
  search-results screenshot evidence for all 326 queries (`326-query/google-images/`,
  `326-query/curify/`) — unscored visual evidence, not a new evaluation. See its README's
  "Known limitations."

Validate with `python3 ../scripts/validate_data.py` (schema/CSV/provenance checks) and
`python3 ../scripts/validate_benchmark.py` (adds image/gallery/hash/credential checks) from the
repository root.
