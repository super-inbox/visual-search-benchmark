# Publication copy (drafts — not published)

Draft social/community copy for the `v1.1.0` release (68-query cross-platform image evidence added).
**Nothing in this file has been posted anywhere.** All platform-specific rules below are drafting
guesses about typical community norms, not confirmed current rules — **manually verify each
community's current posting rules before publishing**, per the pre-publication checklist at the end.

Repo: `https://github.com/super-inbox/visual-search-benchmark` — verify this URL is correct/live
before using it in any of the copy below.

---

## Hacker News

### Title candidates (pick one — Show HN convention)

1. `Show HN: A visual search benchmark with real cross-platform screenshots, not just a query list`
2. `Show HN: Visual Search Benchmark – query, platform, and screenshot evidence side by side`
3. `Show HN: We published our search-relevance eval data, including where it failed`

### Post body

> We ran two internal search-quality evaluations at Curify (a visual/design search product) and
> decided to publish the underlying data instead of just a summary post.
>
> - A 68-query "gold set" testing our own search relevance (LLM-judged, single pass).
> - For 12 of those 68 queries, we also have real screenshots across Curify, Bing Images, Google
>   Images, Canva, and Pinterest — so you can actually see what each platform returned for the same
>   query, not just a score. There's an offline gallery (`data/68-query/gallery/index.html`) you can
>   open locally with no server — filter by query, platform, label, or mapping confidence.
> - A separate, broader 326-query regression set (163 English / 163 Chinese) comparing two states of
>   our own search pipeline — no images, just structured relevance labels.
>
> We tried to be upfront about what this data isn't: the image evidence only covers 12 of the 68
> queries (that's a real limit of what we captured, not a curation choice), neither dataset has
> completed human review, and it's not a scored cross-platform ranking — the competitor screenshots
> come with free-text observations, not numbers. Full methodology, source hashes, and a "known
> limitations" list are in the repo.
>
> We're mainly looking for feedback on: whether the mapping-confidence / evidence-chain approach
> (confirmed vs. probable vs. unknown, with the reasoning written out) is useful for other people
> publishing eval data, whether the gallery format is actually usable, and any data-quality issues
> you spot (there's a validator script and we'd rather know about problems than not).

### First comment (self-post, drafted for after submission)

> A few things worth calling out up front since HN will find them anyway:
>
> - The 62 published images are full-page screenshots, not individual ranked results — so there's
>   no "rank" field to report, and we say so explicitly rather than making one up.
> - All 12 of the queries with image evidence happen to be cases where our own search failed
>   (FAIL label) — that's because the 12-query pilot was originally scoped to already-flagged
>   problem queries, not because we cherry-picked only failures to publish. The full 68-query label
>   distribution (43 FAIL / 25 WARN / 0 PASS) is in the CSV.
> - The competitor screenshots are published as benchmark evidence, not under the same CC BY license
>   as our own data — happy to discuss the licensing approach if anyone has a cleaner suggestion.

---

## Reddit

### r/datasets

**Title:** `[Dataset] Visual/design search benchmark: 68 curated queries + real cross-platform screenshots for 12 of them, 326-query regression set`

**Body:**

> Sharing two internal search-evaluation datasets we just published, CC BY 4.0 for the query/label
> data (screenshots have a separate rights note — see below).
>
> - **68-query benchmark:** hand-curated queries, LLM-judged relevance labels, and — for 12 of the
>   68 — real screenshots across 5 platforms (Curify/Bing/Google/Canva/Pinterest) with a filterable
>   offline gallery.
> - **326-query benchmark:** 326 queries (163 zh/163 en), two evaluation runs (production vs. a
>   candidate pipeline change), no images.
>
> Full schema docs, provenance/hash records, and a validator script are included. We were explicit
> in the docs about what's missing (image coverage is partial, no human-review data in this release,
> not a scored cross-platform ranking) rather than glossing over it.
>
> Repo: `https://github.com/super-inbox/visual-search-benchmark`

**Suggested discussion questions:**
- Is the `confirmed`/`probable`/`unknown` mapping-confidence field a useful pattern for other
  eval-data releases, or overkill?
- Anything missing from the schema that would make this more reusable for your own eval work?

**Avoid:**
- Do not describe this as "the first" or "only" benchmark of its kind.
- Do not claim it's a ranking/leaderboard for Curify vs. competitors — it explicitly isn't.
- Avoid product-pitch language ("game-changing," "revolutionary") — this is a data release, not an
  ad.

### r/computervision

**Title:** `Cross-platform visual search screenshots (Curify/Bing/Google/Canva/Pinterest) for 12 queries, with an offline comparison gallery`

**Body:**

> Not a model release — a data release. We evaluated our own visual/design search product against
> 68 curated queries, and for a 12-query subset also captured real screenshots from 4 other
> image/design platforms for the same queries, so you can visually compare what each one returned.
>
> All images are full-page screenshots (not cropped single results), so there's no per-result rank —
> that's called out explicitly rather than invented. Each image has a mapping-confidence field and
> (where one exists) a relevance label with a written reason. There's a static, offline gallery
> (open the HTML file locally, no server) to browse it.
>
> Also included: a broader 326-query, bilingual regression benchmark for a different part of the
> same search pipeline (no images).
>
> Repo: `https://github.com/super-inbox/visual-search-benchmark`

**Suggested discussion questions:**
- Useful for anyone doing multimodal/visual retrieval eval work as a small qualitative comparison
  set — interested in what additional metadata would make it more useful.
- Anyone have a preferred approach to licensing third-party screenshot evidence in a benchmark
  release? Open question we flagged rather than resolved unilaterally.

**Avoid:**
- Don't oversell this as a large-scale CV benchmark — it's small (62 images) and qualitative for the
  cross-platform part.
- Don't imply the screenshots are freely licensed for training — they're evidence-only, see the
  repo's rights doc.

### r/MachineLearning

**Title:** `[D] Publishing search-relevance eval data with visible failures, not just scores — 68-query + 326-query visual search benchmark`

**Body:**

> We publish a lot of internal eval data at Curify but usually only the summary numbers make it out.
> This time we published the underlying data for two internal search-relevance evaluations, plus
> (for a 12-query subset of one of them) the actual screenshots showing what different platforms
> returned for the same query — so a reader can see the failure mode, not just a FAIL count.
>
> Methodologically: 68-query uses a single-pass LLM (Claude) relevance judge; 326-query uses a
> deterministic-rubric LLM judge (`gpt-4o-mini`, temp 0) comparing two pipeline code states. Neither
> includes completed human review in this release — we say so directly rather than implying
> otherwise. Full rubric text and known limitations are in `METHODOLOGY.md`.
>
> Curious whether people think LLM-judge-only eval releases like this are useful as-is, or whether
> the lack of human-reviewed ground truth is disqualifying for most use cases people would want.
>
> Repo: `https://github.com/super-inbox/visual-search-benchmark`

**Suggested discussion questions:**
- Where do people draw the line on "LLM-judge-only" data being useful vs. needing human review
  before it's citable?
- Is the explicit `mapping_confidence` (confirmed/probable/unknown) approach something you'd want
  to see in other eval-data releases?

**Avoid:**
- Don't frame this as a new SOTA benchmark or leaderboard.
- Don't claim broader generalizability than the query curation supports (see "Social impact/biases"
  in `DATASET_CARD.md`).

### Note on subreddit rules

This draft does **not** claim to have checked r/datasets, r/computervision, or r/MachineLearning's
current posting rules (self-promotion policy, flair requirements, karma/age minimums, etc.).
**Manually verify each subreddit's current rules immediately before posting** — see the checklist
below.

---

## LinkedIn

### Formal version

> We've published two internal search-evaluation datasets from our work on Curify's visual/design
> search: a 68-query curated benchmark — including real cross-platform screenshot evidence for 12
> of those queries, comparing our results against Bing, Google, Canva, and Pinterest for the same
> search — and a separate 326-query, bilingual (Chinese/English) regression benchmark comparing two
> states of our search-relevance pipeline.
>
> We built this to make search-quality evaluation legible: not just a pass/fail score, but the
> actual query, the actual platform, the actual result, and a written reason, wherever our source
> data allowed us to establish that chain with confidence. Where it didn't — most of the 68 queries
> have no cross-platform image evidence, and the 326-query set has none at all — we said so
> explicitly rather than filling the gap with assumptions.
>
> The two datasets are complementary, not redundant: the 68-query set gives depth (visible evidence
> for a subset of cases), the 326-query set gives breadth (broader coverage for regression testing).
>
> Full data, methodology, and an offline browsable image gallery: [GitHub link]
> (`https://github.com/super-inbox/visual-search-benchmark`)

### Concise version

> Published our internal search-eval data: a 68-query benchmark with real cross-platform screenshots
> (Curify vs. Bing/Google/Canva/Pinterest) for 12 of those queries, plus a broader 326-query,
> bilingual regression benchmark. Query, platform, image, and judgment — tied together with an
> explicit confidence rating, not guessed. Link: [GitHub link]

### Technical-team-share version

> Data drop: two search-eval datasets, CC BY 4.0 (data/labels; screenshots have a separate rights
> note in the repo).
>
> - 68-query gold set, LLM-judged (Claude), + 62 real cross-platform screenshots for a 12-query
>   subset (Curify/Bing/Google/Canva/Pinterest) with SHA-256-verified provenance and an offline
>   filterable gallery (`gallery/index.html`, no server needed).
> - 326-query bilingual regression set, two pipeline states, LLM-judge (`gpt-4o-mini`, temp 0,
>   documented rubric).
> - Includes a validator script, a full source-audit doc, and an explicit `mapping_confidence`
>   field (confirmed/probable/unknown) on every image record instead of implying certainty that
>   isn't there.
>
> Repo: `https://github.com/super-inbox/visual-search-benchmark`

---

---

## 老板工作汇报（中文，简洁版）

**68-query 图片补充情况：** 已从内部 adhoc 仓库中定位到 68 个 query 中真正带跨平台图片证据的子集 ——
仅 **12 个 query**（并非全部 68 个），每个 query 有 Curify / Bing / Google / Canva / Pinterest
五个平台的真实搜索结果截图（共 62 张，含 1 个 query 的 2 张备份截图），已逐张计算 SHA-256、验证可解码、
按统一命名规则复制进公开仓库（原图未做任何裁剪/修改）。其余 56 个 query 在源仓库中确实没有任何跨平台
图片证据，这是数据本身的局限，本次没有补拍或伪造。

**GitHub 仓库新增内容：**
1. `data/68-query/images/` —— 62 张截图，按平台分文件夹存放。
2. `data/68-query/gallery/index.html` —— 离线可用的图片对比 gallery，支持按 query/平台/标签/图片类型/
   映射置信度筛选，双击本地打开即可用，无需联网或起服务。
3. `data/68-query/results.jsonl` + `image_manifest.json` + `IMAGE_MAPPING_REPORT.md` —— 统一的图片
   元数据（含 rank=UNKNOWN 的明确标注、mapping_confidence 全部为 confirmed）。
4. `docs/68_IMAGE_SOURCE_INVENTORY.md`、`docs/EXAMPLE_CROSS_PLATFORM_COMPARISONS.md`、
   `docs/IMAGE_RIGHTS_AND_ATTRIBUTION_REVIEW.md` —— 数据来源盘点、8 个精选案例对比、图片版权说明。
5. README / DATASET_CARD / 各子 README 已更新，明确区分 68-query（有部分图片证据）与 326-query（完全
   无图片）的定位，避免误导读者。
6. `scripts/validate_benchmark.py` + `VALIDATION_REPORT.md` + `SIZE_REPORT.md` —— 补充了图片哈希校验、
   gallery 引用校验、敏感信息扫描、仓库体积评估。

**326-query 为何没有新增跨平台图片：** 按你的要求，本次未对 326-query 做任何新的搜索或抓图。核实后确认
adhoc 仓库中不存在任何 326-query 对应的跨平台图片素材；唯一相关的跨平台图片资产是一个完全不同的
58-query 试点（与 68-query、326-query 均无 query 重合），已在 inventory 报告中记录但未纳入本次发布。

**发布文案准备情况：** Hacker News（3 个标题候选 + 正文 + 首条评论）、Reddit（r/datasets、
r/computervision、r/MachineLearning 三个版本，含讨论问题和应避免用语）、LinkedIn（正式版/简洁版/技术
团队版）均已起草完毕，见 `docs/release/PUBLICATION_COPY.md`。**均未发布**，且文案中已注明需要人工在
发布前逐一核实各平台最新规则。

**需要你确认的事项：**
1. 12/68 的图片覆盖范围是否符合预期，是否需要补充说明或调整对外表述。
2. `LICENSE` 中新增的"第三方截图不适用 CC BY 4.0"条款表述是否可以直接使用，还是需要法务介入
   （见 `docs/IMAGE_RIGHTS_AND_ATTRIBUTION_REVIEW.md` 最后的"Open question"部分）。
3. 发布文案的语气、GitHub 链接是否正确、是否要用公司账号还是个人账号发布。
4. 仓库体积（新增约 158MB 图片，见 `SIZE_REPORT.md`）是否需要在 push 前处理（例如 Git LFS），本次
   未擅自启用 LFS 或压缩图片。
5. 是否同意现在 commit / push——按你的要求，本次尚未执行任何 commit 或 push。

---

## Pre-publication checklist (manual, before any of the above goes out)

- [ ] Confirm the GitHub repo URL is correct and the repository is actually public.
- [ ] Manually re-check current posting/self-promotion rules for r/datasets, r/computervision, and
      r/MachineLearning (they change; this draft does not assume any specific current ruleset).
- [ ] Confirm HN's current Show HN guidelines (e.g. no other simultaneous submissions, etc.).
- [ ] Have someone outside this project skim `docs/IMAGE_RIGHTS_AND_ATTRIBUTION_REVIEW.md` before
      any public post references the screenshots, in case the licensing framing needs adjustment.
- [ ] Decide who (which named person / company account) is posting, and adjust "we" phrasing if a
      single named author is posting instead of a company account.
- [ ] Nothing in this file should be posted verbatim without a final human read-through for tone.
