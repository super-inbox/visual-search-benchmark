# Visual Search Benchmark

Two curated internal evaluation datasets from [Curify](https://curify-ai.com), converted for public
release: a 68-query gold set evaluating Curify's own search relevance, and a 326-query regression
benchmark comparing two states of Curify's search-relevance pipeline. Intended for reproducible
reference and comparison, not as an industry-standard or complete benchmark of visual/design search.

> **Status:** data published, `v1.0.0`. See [`METHODOLOGY.md`](METHODOLOGY.md) for how each
> benchmark was built, and [`SOURCE_AUDIT.md`](SOURCE_AUDIT.md) for source provenance and hashes.

## Benchmarks at a glance

| | 68-query | 326-query |
|---|---|---|
| Queries | 68, hand-curated | 326 (163 zh / 163 en) |
| System(s) evaluated | Curify only | Curify only — production baseline vs. a candidate branch |
| Cross-platform? | No (a separate, unpublished 12-query pilot has screenshots only, no scores) | No |
| Judging | Single-pass LLM (Claude) relevance label | LLM judge (`gpt-4o-mini`), PASS/PARTIAL/FAIL/UNJUDGABLE |
| Human review | Not included in this public release | Not included in this public release |
| Labels | `PASS` / `WARN` / `FAIL` | `PASS` / `PARTIAL` / `FAIL` / `UNJUDGABLE` |

**The two benchmarks are intentionally not merged into one schema** — different query sets,
different systems under test, different label vocabularies. See [`METHODOLOGY.md`](METHODOLOGY.md)
for why, and each dataset's own `data/*/README.md` for details.

## Directory structure

```
data/
  68-query/
    README.md                        per-dataset documentation
    queries.csv                      68 curated queries + curation metadata
    automated_relevance_labels.csv   Curify search collection + LLM relevance label
    schema.json                      field definitions
    provenance.json                  source hashes and transformation notes
  326-query/
    README.md
    queries.csv                      326 queries with stable IDs (V001-V326)
    evaluations.csv                  production-baseline + candidate run results (652 rows)
    schema.json
    provenance.json
scripts/
  validate_data.py                  integrity + schema validator (see below)
METHODOLOGY.md                       full methodology for both benchmarks
SOURCE_AUDIT.md                      source selection evidence and hashes
VALIDATION_REPORT.md                 result of the validation/QA pass for this release
```

## Quick start

```python
import pandas as pd

q68 = pd.read_csv("data/68-query/queries.csv")
labels68 = pd.read_csv("data/68-query/automated_relevance_labels.csv")

q326 = pd.read_csv("data/326-query/queries.csv")
evals326 = pd.read_csv("data/326-query/evaluations.csv")
evals326.groupby("run_variant")["relevance_label"].value_counts()
```

## Validation

```
python3 scripts/validate_data.py
```

Checks file structure, encoding, duplicate/empty queries, referential integrity between queries
and evaluation rows, label-vocabulary conformance, provenance-hash consistency, and scans for
accidentally-included local paths or secrets. See [`VALIDATION_REPORT.md`](VALIDATION_REPORT.md)
for the result recorded at release time.

## Limitations

- Neither benchmark is a cross-platform comparison of Curify against other search or design
  platforms, despite earlier internal planning documents proposing one — see `METHODOLOGY.md`.
- Relevance labels in both benchmarks are primarily LLM-judge output, not human review. Read each
  dataset's README for exactly how much (if any) human verification exists.
- The 326-query candidate branch evaluated here was explicitly not approved for production at the
  time of capture; treat it as a regression-testing snapshot.
- Both are point-in-time snapshots; results will differ from current production Curify search.

## License

Data: **CC BY 4.0** (see [`LICENSE`](LICENSE)) — free to use with attribution.

## Citation

See [`CITATION.cff`](CITATION.cff).

## About Curify

[Curify AI](https://curify-ai.com) is an applied-AI company building the **deterministic production layer above foundation models** — reliable, traceable, enterprise-grade pipelines, not a prompt wrapper. Our products span two lines:

- **Enterprise AI** — an industrial-grade multimodal content engine + enterprise **document intelligence** (RAG with mandatory source citation, structured extraction, on-premise; *deterministic · traceable · data stays yours*).
- **AI-Native Product** — creator / SMB-facing generation at [curify-ai.com](https://curify-ai.com): structured data & long-tail keywords → thousands of on-brand visual assets, multilingual video, and one-click design tools.

**Links** · Website: [curify-ai.com](https://curify-ai.com) · Mentorship (founder, Jay Wang): [mentorcruise.com/mentor/jaywang](https://mentorcruise.com/mentor/jaywang/)
