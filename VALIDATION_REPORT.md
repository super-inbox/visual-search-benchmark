# Validation Report

Generated 2026-07-30 for the initial public data release (`v1.0.0`) of both benchmarks. This
report reflects actual results from running `scripts/validate_data.py` and manual spot-checks
against the internal source repository, not expected/assumed results.

## Public file list

```
README.md
data/README.md
LICENSE
CITATION.cff
METHODOLOGY.md
SOURCE_AUDIT.md
VALIDATION_REPORT.md
scripts/validate_data.py
data/68-query/README.md
data/68-query/queries.csv
data/68-query/automated_relevance_labels.csv
data/68-query/schema.json
data/68-query/provenance.json
data/326-query/README.md
data/326-query/queries.csv
data/326-query/evaluations.csv
data/326-query/human_spot_check.csv
data/326-query/schema.json
data/326-query/provenance.json
```

## Source and public hashes

| Public file | SHA-256 | Source file | Source SHA-256 |
|---|---|---|---|
| `data/68-query/queries.csv` | `038314e456ca342489578a83f0edbd1a79b8a8a457f7ee5684d64ed741fe52db` | `gold_query_test_set_2026-07-07.csv` | `00bd2cff0f1dee8168c366020198ed592d0f9654786ff417aa00a19ba4c7ae68` |
| `data/68-query/automated_relevance_labels.csv` | `c71a1617afbfe4e4ea78978b61dee82c1487717d8d27d3f8af3a350937d4ab98` | `curify_search_auto_collect_with_claude_relevance_2026-07-07.csv` | `a1a7381927f13b6592e3bcd60eeb49c3da9642be878096b5f833083bf884d897` |
| `data/326-query/queries.csv` | `d8ae0f4ef77567b4dcf8f15635b11c140810c3b991a8134a99997e11ad6a1d9e` | `easy_query_bank_v2_2026-07-16.csv` (+ `easy_query_v2_input_with_ids.csv`) | `c5b1368e33ab601884ad91aff21802c64391bee781b6daa2f3ef50e4d54a08c6` / `f51bd68e2139cfcca72a5235df6140b75e57c86574353ccf319645de7c13fa7a` |
| `data/326-query/evaluations.csv` | `99a658808166988dcd775b4ff5ce82e8f190b43445bbb0848029cc1f14606c4c` | `BASELINE_EASY326.csv` (+ `03_FULL326_LATEST_RESULTS.csv`) | `0b8d15173c5a86a683c5d1e84a93c13fc5fcc75b4e2ffc4e44565a6a1af3d9fa` / `08c1b6a5e89c94066f37715d90f49e25ed19a6a017eb0e53c2c9fbdebc24c4eb` |
| `data/326-query/human_spot_check.csv` | `ec3186cbd122dd4bd8e11096cbaba8088f774883ccd5afb9fd96cb96a786c3eb` | `326人工核验.xlsx` | `9a18b052e3b64ad4c350cd5c7c7d91c56ecf327413f0f112a5dc2751d3643fdd` |

All public-file hashes above were recomputed at report time and match the values recorded in each
dataset's `provenance.json` — confirmed automatically by `scripts/validate_data.py`.

## Query, language, category/scenario counts

**68-query:** 68 unique queries, 0 duplicates, 0 empty. Language: English 34 / Chinese 28 / mixed 6.
Scene: brand 19 / marketing-ecommerce 18 / education 17 / cultural-creative 14.

**326-query:** 326 unique queries, 0 duplicates, 0 empty. Language: 163 zh / 163 en exactly.
Scenario: creative_merch 82 / brand_business 82 / marketing_ecommerce 82 / education 80.

## Status / label distributions

**68-query** (`claude_relevance_label`): FAIL 43, WARN 25, PASS 0.

**326-query** (`relevance_label`, by `run_variant`):

| run_variant | PASS | PARTIAL | FAIL | UNJUDGABLE | zero_result | low_result |
|---|---|---|---|---|---|---|
| production_baseline_2026-07-21 | 24 | 83 | 207 | 12 | 23 | 19 |
| candidate_2026-07-22_0e794cd9 | 38 | 86 | 195 | 7 | 20 | 18 |

**326-query human spot-check** (`human_verdict`): FAIL 160, PARTIAL 64, PASS 48, PARTIAL? 30,
UNJUDGABLE 6, PASS？ 3, PASS? 3, blank (not reviewed) 12. Total reviewed: 314/326.

## Duplicate / missing-value checks

No duplicate `query_id` in any file. No duplicate normalized query text in any query list. No
empty query text anywhere. All checks executed by `scripts/validate_data.py`.

## Referential integrity

- 68-query: all 68 `automated_relevance_labels.csv` rows join to a `queries.csv` query_id; no
  unexpected or missing IDs.
- 326-query: both `evaluations.csv` run variants (326 rows each, 652 total) and
  `human_spot_check.csv` (326 rows) join fully to `queries.csv` query_id; no unexpected or missing
  IDs.

## Sensitive-data scan

No secret scanner (gitleaks/trufflehog/detect-secrets) was installed in this environment; a
multi-pattern grep sweep plus a Python regex pass were run instead over every file staged for this
release, checking for: local absolute paths (`/Users/`, `/home/`), `file://` URLs, `localhost`/
`127.0.0.1`, and credential-shaped strings (`API_KEY`, `SECRET`, `PASSWORD`, `AUTHORIZATION`,
`BEARER`, `COOKIE`, `SESSION`, `PRIVATE KEY`, `ghp_`, `github_pat_`, `sk-`).

**Result:** one match, in `SOURCE_AUDIT.md` itself — the substring `sk-` inside the public Curify
template slug `elon-musk-tech-meme` (part of a documented, reviewed false-positive explanation).
Confirmed not a credential: it is a public product-catalog template identifier, quoted here only
to explain why the pattern match is safe. No other matches in any file. No `.DS_Store`,
`__pycache__`, editor lock files, or unexpected binary files are present among the staged files.

## Source-to-public spot checks

10 deterministic records were compared per dataset (first, last, evenly-spaced middle records,
spanning both languages, multiple scene/scenario categories, and multiple label values). All 20
records matched their source rows exactly on query text, and on every evaluation field checked
(relevance label, result counts). Full spot-check output:

**68-query** (index = row position in the gold-set file, 0-based):

| idx | query_id | query (truncated) | scene | claude label | match |
|---|---|---|---|---|---|
| 0 | q001 | Love and Deepspace card pack design | 文创 | FAIL | OK |
| 6 | q007 | meme格式国风梗图模板 | 文创 | WARN | OK |
| 13 | q014 | 谷圈应援色贴纸设计 | 文创 | WARN | OK |
| 20 | q021 | 二手奢侈品鉴定品牌视觉 | 品牌 | FAIL | OK |
| 27 | q028 | 宠物殡葬服务品牌视觉设计 | 品牌 | WARN | OK |
| 33 | q034 | Amazon EBC enhanced brand content layout | 营销电商 | FAIL | OK |
| 40 | q041 | 小红书对比图 use前后 | 营销电商 | WARN | OK |
| 47 | q048 | 抖音带货主播人设海报 | 营销电商 | WARN | OK |
| 54 | q055 | RTI intervention tracker template | 教育 | FAIL | OK |
| 67 | q068 | zones of regulation poster classroom | 教育 | FAIL | OK |

**326-query** (index = row position in the query bank, 0-based):

| idx | query_id | query | lang | scenario | baseline | candidate | human | match |
|---|---|---|---|---|---|---|---|---|
| 0 | V001 | 玩具 | zh | creative_merch | FAIL | PARTIAL | FAIL | OK |
| 35 | V036 | phone case | en | creative_merch | FAIL | FAIL | PASS？ | OK |
| 70 | V071 | 动漫周边 | zh | creative_merch | PASS | PASS | PARTIAL? | OK |
| 105 | V106 | tea package | en | brand_business | FAIL | FAIL | PARTIAL? | OK |
| 140 | V141 | 蜡烛标签 | zh | brand_business | FAIL | UNJUDGABLE | FAIL | OK |
| 162 | V163 | 月饼礼盒 | zh | brand_business | FAIL | FAIL | FAIL | OK |
| 163 | V164 | mooncake gift box | en | brand_business | FAIL | FAIL | FAIL | OK |
| 200 | V201 | 节日促销横幅 | zh | marketing_ecommerce | PARTIAL | PARTIAL | PARTIAL? | OK |
| 250 | V251 | 字母卡 | zh | education | UNJUDGABLE | PASS | PASS | OK |
| 325 | V326 | reward chart | en | education | FAIL | FAIL | FAIL | OK |

## Known limitations

See each dataset's `README.md` and `provenance.json`, and the root `METHODOLOGY.md`. In summary:
neither benchmark is cross-platform; the 68-query set has no completed human review; the
326-query set's candidate branch was not approved for production at capture time; and the human
spot-check for the 326-query set covers 314 of 326 rows.

## Overall result

- `python3 scripts/validate_data.py` → **PASS** (exit code 0)
- `git diff --check` → clean, no whitespace errors
- Sensitive-data scan → clean (one reviewed false positive, documented above)
- Spot checks (20 records) → all matched source exactly

**OVERALL: PASS**
