# AI Design Benchmark

A public, human-scored benchmark for **visual-design search & discovery** — how well different
surfaces answer real design/merch/education queries. Built and maintained by
[Curify](https://curify-ai.com).

> **Status:** scaffold — data drop pending. Methodology below is final; the scored data
> (v1 = 68 queries, v2 = 326 queries) lands in [`data/`](data/).

## What this measures

For each query, the top results from several surfaces are scored by human reviewers on three
dimensions. The point is **not** to rank-correlate against any single site, but to measure
*where each surface actually wins*.

**Surfaces compared** (top-N results per query):

| Surface | Source |
|---|---|
| Curify | `/search?q=<query>` — top-20 inspirations |
| Pinterest | top pins |
| Bing Images | top results |
| Google Images | top results |
| Canva | template search |

**Scoring dimensions** (0–5 each, per surface, per query):

| Dimension | Question |
|---|---|
| **Relevance** | Does each result look like what the user asked for? |
| **Diversity** | Are results visually / topically varied, or all the same? |
| **Actionability** | Can the user *do* something with it — copy, remix, generate, edit? |

Per query → a 5×3 score matrix (15 numbers). Aggregated across query buckets to surface
category leaders. First pass is **manual** (1–2 reviewers); a rubric / LLM-rater is trained
once ~30 queries are scored, for scale.

## Versions

| Version | Queries | Notes |
|---|---|---|
| **v1** | 68 | first scored set |
| **v2** | 326 | expanded set (superset direction) |

Each version is a tagged release; the CSVs are versioned so a citation always resolves to a
fixed snapshot.

## Data format (`data/`)

`queries.csv`
```
query_id,query,bucket
q001,brazil world cup poster,sports-poster
...
```

`scores.csv`
```
query_id,surface,relevance,diversity,actionability,reviewer,notes
q001,curify,5,4,5,baobao,
q001,pinterest,4,5,2,baobao,
...
```

> Field names are a proposal — align to Baobao's actual export; keep it CSV/JSONL + a fixed schema.

## Use

```python
import pandas as pd
q = pd.read_csv("data/queries.csv")
s = pd.read_csv("data/scores.csv")
# mean actionability by surface:
s.groupby("surface")["actionability"].mean()
```

## Links

- Research page & findings: https://curify-ai.com/resources/ai-design-benchmark
- Hugging Face dataset (mirror): `curify/ai-design-benchmark`
- Catalog: `curify-datasets`

## License

Data: **CC BY 4.0** (see [`LICENSE`](LICENSE)) — free to use with attribution.

## Citation

See [`CITATION.cff`](CITATION.cff), or:

> Curify (2026). *AI Design Benchmark: human-scored visual-design search evaluation.*
> https://curify-ai.com/resources/ai-design-benchmark

## About Curify

[Curify AI](https://curify-ai.com) is an applied-AI company building the **deterministic production layer above foundation models** — reliable, traceable, enterprise-grade pipelines, not a prompt wrapper. Our products span two lines:

- **Enterprise AI** — an industrial-grade multimodal content engine + enterprise **document intelligence** (RAG with mandatory source citation, structured extraction, on-premise; *deterministic · traceable · data stays yours*).
- **AI-Native Product** — creator / SMB-facing generation at [curify-ai.com](https://curify-ai.com): structured data & long-tail keywords → thousands of on-brand visual assets, multilingual video, and one-click design tools.

**Links** · Website: [curify-ai.com](https://curify-ai.com) · Mentorship (founder, Jay Wang): [mentorcruise.com/mentor/jaywang](https://mentorcruise.com/mentor/jaywang/)
