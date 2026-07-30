# 68-query IMAGE_MAPPING_REPORT

Generated from `image_manifest.json` and `results.jsonl`. Total published image records: 62.

## Confirmed mappings

All 62 published image records have `mapping_confidence: confirmed` for query_id and platform. See `docs/68_IMAGE_SOURCE_INVENTORY.md` section 5 for the evidence chain. Per-query breakdown:

| query_id | query | platforms present | curify evaluation_label |
|---|---|---|---|
| q002 | NCT Dream photocard template | bing, canva, curify, google, pinterest | FAIL |
| q006 | genshin impact Furina fanart wallpaper 4k | bing, canva, curify, google, pinterest | FAIL |
| q009 | 低饱和国风茶包装设计 | bing, canva, curify, google, pinterest | FAIL |
| q010 | 光与夜之恋 卡面设计参考图 | bing, canva, curify, google, pinterest | FAIL |
| q015 | K-beauty glass skin brand launch visual | bing, canva, curify, google, pinterest | FAIL |
| q016 | Y2K chrome skincare launch poster | bing, canva, curify, google, pinterest | FAIL |
| q034 | Amazon EBC enhanced brand content layout | bing, canva, curify, google, pinterest | FAIL |
| q046 | 小红书香薰产品种草图 | bing, canva, curify, google, pinterest | FAIL |
| q053 | IEP accommodations checklist visual | bing, canva, curify, google, pinterest | FAIL |
| q060 | coding unplugged activity cards | bing, canva, curify, google, pinterest | FAIL |
| q064 | maker space label set printable | bing, canva, curify, google, pinterest | FAIL |
| q068 | zones of regulation poster classroom | bing, canva, curify, google, pinterest | FAIL |

## Probable mappings

None. Every image in this release has `confirmed` mapping confidence -- there are no `probable`-confidence images in this batch.

## Unknown mappings

None. No image was published with `mapping_confidence: unknown` -- any image whose query or platform could not be confirmed was excluded rather than guessed (none were found in this 12-query asset; the 58-query pilot with zero query overlap was excluded entirely at the dataset level, not the image level -- see the inventory doc).

## Missing images

The other 56 of 68 queries have no cross-platform image evidence anywhere in the source repository. This is a data-availability gap, not a publishing omission. See `docs/68_IMAGE_SOURCE_INVENTORY.md`.

## Duplicate images

- SHA-256 `451124ef984231bd...` shared by: data/68-query/images/curify/q015__curify__rank_UNKNOWN__1.png, data/68-query/images/curify/q015__curify__rank_UNKNOWN__2.png (query q015 / K-beauty glass skin brand launch visual -- `curify1.png` was copied verbatim to become the primary `curify.png`; both are published, see the `notes` field on each record).

## Broken images

None. 62/62 images decoded successfully (Pillow verify + re-open pass).

## Missing platforms

None for the 12 covered queries -- every one of the 12 has all 5 platforms (Curify, Bing, Google, Canva, Pinterest). No platform is missing for any covered query.

## Missing ranks

All 62 images have `organic_rank: null`. These are full-page SERP screenshots, not single ranked results -- no source document assigns a rank to any individual result inside them, so rank is UNKNOWN by design for 100% of this asset (not a partial gap).

## Fields that could not be confirmed (left null/UNKNOWN)

- `organic_rank` -- null for all 62 (see above).
- `image_source_url` -- null for all 62 (no individual per-image source URL was ever recorded; these are full-page screenshots of search result pages, not saved individual images with their own URLs).
- `source_page_url` -- populated only for the 12 `curify` images (from the already-published `search_url` column in `automated_relevance_labels.csv`); null for the 50 competitor-platform images, since no source document recorded the exact search URL used for Bing/Google/Canva/Pinterest captures.
- `evaluation_label` -- populated only for the 12 `curify` images (`FAIL` for all 12, matching the already-published `claude_relevance_label`); null for the 50 competitor-platform images, which only have free-text observations, not a formal label.
