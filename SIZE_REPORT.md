# Size Report

Generated 2026-07-31 alongside the `v1.1.0` update (68-query cross-platform image evidence added).

## New content added this update

| Item | Size | File count |
|---|---|---|
| `data/68-query/images/` (62 PNG screenshots) | ~158 MB | 62 |
| `data/68-query/gallery/thumbnails/` (62 JPEG thumbnails) | ~2.6 MB | 62 |
| `data/68-query/gallery/index.html` | ~50 KB | 1 |
| `data/68-query/results.jsonl` + `image_manifest.json` + `IMAGE_MAPPING_REPORT.md` | < 200 KB combined | 3 |
| New/updated docs (`docs/`, `SIZE_REPORT.md`, `DATASET_CARD.md`, etc.) | < 200 KB combined | ~10 |
| **Total new working-tree size added** | **~161 MB** | **~140 files** |

## Largest individual files

| File | Size |
|---|---|
| `data/68-query/images/pinterest/q010__pinterest__rank_UNKNOWN__1.png` | 7.4 MB |
| `data/68-query/images/pinterest/q006__pinterest__rank_UNKNOWN__1.png` | 6.8 MB |
| `data/68-query/images/pinterest/q002__pinterest__rank_UNKNOWN__1.png` | 6.2 MB |
| `data/68-query/images/pinterest/q015__pinterest__rank_UNKNOWN__1.png` | 5.4 MB |
| `data/68-query/images/pinterest/q034__pinterest__rank_UNKNOWN__1.png` | 5.4 MB |

**No file in this repository exceeds GitHub's 100 MB hard per-file limit, and none exceed the 50 MB
soft-warning threshold either** (largest is ~7.4 MB). No Git LFS requirement is triggered by file
size alone.

## Repository totals (working tree, excluding `.git`)

- Full working tree: ~161 MB (up from a few hundred KB pre-`v1.1.0`, almost entirely the 158 MB of
  PNG screenshots).
- `.git` directory (existing history, before this update is committed): ~356 KB.

## Will this make the repo "too large"?

Not in absolute terms — 161 MB is well within normal ranges for a GitHub repository (GitHub's own
soft guidance is to keep repos under ~1 GB, hard-warns past 5 GB for most plans). The main practical
consideration is that **once committed, these 62 binary PNGs become permanent history** — every
future `git clone` downloads them, and any future edit to an image would double-store both versions
(Git does not diff binaries efficiently). Since these are original evidence images that should never
be edited in place (per the "don't modify evidence images" rule), this is a one-time cost, not a
growing one, but it's worth the user's awareness before committing.

## Options if the user wants to reduce this footprint (none applied automatically)

1. **Do nothing.** 161 MB is not large enough to require any special handling; this is the default
   recommendation.
2. **Git LFS for `data/68-query/images/*.png`.** Would keep the main repo history small and store
   the binaries separately. **Not enabled in this pass** — enabling LFS changes how clones/CI/forks
   behave and is a decision for the user, not something to switch on unilaterally.
3. **Keep only thumbnails in Git, host full-resolution originals elsewhere** (e.g. a release asset
   or object storage), linking out from the gallery. Would shrink the tracked repo to ~3 MB of
   images. Not applied — this would change the "self-contained, no external dependencies" property
   of the current gallery and requires the user to choose and stand up that hosting.
4. **Re-encode PNGs as JPEG/WebP to shrink originals.** Explicitly **not done** — the task
   constraints prohibit modifying or degrading the original evidence images, and lossy re-encoding
   of the *originals* (as opposed to the already-separate thumbnails, which are JPEGs) would violate
   that.

None of these were applied. Thumbnails were generated (as instructed) without touching the
originals; no compression, cropping, LFS migration, or external re-hosting was performed
automatically.
