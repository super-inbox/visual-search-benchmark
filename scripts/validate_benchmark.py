#!/usr/bin/env python3
"""Extended validator for the Visual Search Benchmark public release.

Covers what scripts/validate_data.py does not: the 68-query image evidence
(results.jsonl, image_manifest.json, images/, gallery/), the 326-query
Google Images + Curify screenshot evidence (data/326-query/google-images/,
data/326-query/curify/ -- image decode/format/dimension checks and gallery
reference checks; row-count/referential-integrity checks for those two
manifests live in validate_data.py), plus repo-wide checks for external
references, local absolute paths, and secret-shaped strings.

Runs with: python3 scripts/validate_benchmark.py
Exit code 0 only if every mandatory check passes. Standard library only
(uses the same lightweight decode check as build time; falls back gracefully
if Pillow is not installed).

This script is additive to scripts/validate_data.py, not a replacement for it —
run both. See README.md "Validation".
"""
import csv
import hashlib
import json
import os
import re
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA68 = os.path.join(ROOT, "data", "68-query")
DATA326 = os.path.join(ROOT, "data", "326-query")

failures = []
warnings = []
stats = {}


def fail(msg):
    failures.append(msg)


def warn(msg):
    warnings.append(msg)


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()


SENSITIVE_PATTERNS = [
    # Require at least one real path-character segment after the prefix so that documentation
    # merely *naming* the pattern (e.g. "local absolute paths (`/Users/`, `/home/`)") doesn't
    # self-trigger -- a real leaked path always has a username/subdirectory after the prefix.
    (r"/Users/[A-Za-z0-9_.\-]+(?:/[^\"'\s,]*)?", "local absolute path (/Users/)"),
    (r"/home/[A-Za-z0-9_.\-]+(?:/[^\"'\s,]*)?", "local absolute path (/home/)"),
    (r"\blocalhost\b", "localhost reference"),
    (r"127\.0\.0\.1", "loopback IP"),
    # Word-boundary credential patterns require assignment-like context (":" or "=" after,
    # optionally through quotes) so ordinary English usage ("the secret to glowing skin") and this
    # script's own pattern-name prose don't self-trigger; real leaked credentials are virtually
    # always written as KEY=value or "key": "value".
    (r"\bAPI_KEY\b\s*[:=]", "API_KEY-shaped assignment"),
    (r"\bSECRET\b\s*[:=]", "SECRET-shaped assignment"),
    (r"\bPASSWORD\b\s*[:=]", "PASSWORD-shaped assignment"),
    (r"\bBEARER\s+[A-Za-z0-9_\-\.]{10,}", "BEARER token"),
    (r"\bCOOKIE\b\s*[:=]", "COOKIE-shaped assignment"),
    (r"ghp_[A-Za-z0-9]{10,}", "GitHub personal access token"),
    (r"github_pat_[A-Za-z0-9_]{10,}", "GitHub fine-grained PAT"),
    (r"(?<![A-Za-z0-9_-])sk-[A-Za-z0-9]{10,}", "sk- style API key"),
]
SENSITIVE_RE = [(re.compile(p, re.IGNORECASE), label) for p, label in SENSITIVE_PATTERNS]

# Strings already reviewed and confirmed NOT to be real secrets/paths, documented in
# SOURCE_AUDIT.md / docs/68_IMAGE_SOURCE_INVENTORY.md. Presence of any of these near a match means
# the match is a documented, reviewed false positive, not a new finding.
KNOWN_FALSE_POSITIVES = {"elon-musk-tech-meme", "<username>"}

# This script (and validate_data.py) contain the sensitive-pattern definitions themselves as
# literal regex source text, which would otherwise flag them as containing what they detect.
SELF_EXCLUDE = {"scripts/validate_benchmark.py", "scripts/validate_data.py"}


def scan_text_for_sensitive(path, text):
    rel = path
    if os.path.isabs(path):
        rel = os.path.relpath(path, ROOT)
    if rel.replace(os.sep, "/") in SELF_EXCLUDE:
        return
    for regex, label in SENSITIVE_RE:
        for m in regex.finditer(text):
            hit = m.group(0)
            if any(fp in text[max(0, m.start() - 20):m.end() + 20] for fp in KNOWN_FALSE_POSITIVES):
                continue
            fail(f"{path}: possible {label} found: {hit[:60]!r}")


def load_jsonl(path):
    rows = []
    with open(path, encoding="utf-8") as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as e:
                fail(f"{path}:{i}: invalid JSON line ({e})")
    return rows


def check_image_decodable(path):
    try:
        from PIL import Image
        with Image.open(path) as im:
            im.verify()
        with Image.open(path) as im:
            im.load()
        return True
    except ImportError:
        # Fallback: verify PNG magic bytes only.
        with open(path, "rb") as f:
            header = f.read(8)
        return header == b"\x89PNG\r\n\x1a\n"
    except Exception as e:
        fail(f"{path}: image failed to decode ({e})")
        return False


def check_68query_images():
    results_path = os.path.join(DATA68, "results.jsonl")
    manifest_path = os.path.join(DATA68, "image_manifest.json")
    if not os.path.isfile(results_path):
        fail("data/68-query/results.jsonl: missing")
        return
    if not os.path.isfile(manifest_path):
        fail("data/68-query/image_manifest.json: missing")
        return

    results = load_jsonl(results_path)
    with open(manifest_path, encoding="utf-8") as f:
        manifest = json.load(f)

    stats["results_records"] = len(results)
    stats["manifest_images"] = manifest.get("image_count")

    if len(results) != manifest.get("image_count"):
        fail(f"results.jsonl has {len(results)} records but image_manifest.json image_count is "
             f"{manifest.get('image_count')} -- counts must match")

    seen_paths = set()
    dup_paths = []
    seen_triples = set()
    dup_triples = []
    platform_counts = {}
    confidence_counts = {"confirmed": 0, "probable": 0, "unknown": 0}
    broken = 0
    hash_mismatches = 0

    query_ids = set()
    q68_csv = os.path.join(DATA68, "queries.csv")
    if os.path.isfile(q68_csv):
        with open(q68_csv, encoding="utf-8") as f:
            query_ids = {r["query_id"] for r in csv.DictReader(f)}

    for r in results:
        # required fields present
        for field in ("benchmark_id", "query_id", "query", "platform", "image_path",
                      "mapping_confidence"):
            if field not in r:
                fail(f"results.jsonl record missing required field '{field}': {r}")

        if r.get("query_id") and query_ids and r["query_id"] not in query_ids:
            fail(f"results.jsonl: query_id {r['query_id']!r} not present in queries.csv")

        # organic_rank must be int or null, never a string
        rank = r.get("organic_rank")
        if rank is not None and not isinstance(rank, int):
            fail(f"results.jsonl: organic_rank must be integer or null, got {rank!r} for "
                 f"{r.get('query_id')}/{r.get('platform')}")

        conf = r.get("mapping_confidence")
        if conf not in confidence_counts:
            fail(f"results.jsonl: unexpected mapping_confidence value {conf!r}")
        else:
            confidence_counts[conf] += 1

        if conf == "probable" and not r.get("mapping_evidence"):
            fail(f"results.jsonl: probable-confidence record missing mapping_evidence: "
                 f"{r.get('query_id')}/{r.get('platform')}")

        plat = r.get("platform")
        platform_counts[plat] = platform_counts.get(plat, 0) + 1

        img_path = r.get("image_path")
        if img_path:
            if os.path.isabs(img_path):
                fail(f"results.jsonl: image_path is a local absolute path (must be repo-relative): {img_path}")
            full = os.path.join(ROOT, img_path)
            if not os.path.isfile(full):
                fail(f"results.jsonl: image_path does not exist on disk: {img_path}")
            else:
                key = (r.get("query_id"), plat, rank, img_path)
                triple_key = (r.get("query_id"), plat, rank)
                if img_path in seen_paths:
                    dup_paths.append(img_path)
                seen_paths.add(img_path)
                if triple_key in seen_triples and img_path not in dup_paths:
                    # Same query/platform/rank appearing twice with a *different* file is a real
                    # duplicate-record concern; same file twice is caught above.
                    dup_triples.append(triple_key)
                seen_triples.add(triple_key)

                if not check_image_decodable(full):
                    broken += 1

                actual_hash = sha256_of(full)
                if r.get("published_sha256") and actual_hash != r["published_sha256"]:
                    hash_mismatches += 1
                    fail(f"{img_path}: sha256 {actual_hash} does not match published_sha256 "
                         f"{r['published_sha256']} recorded in results.jsonl")

        thumb_path = r.get("thumbnail_path")
        if thumb_path:
            if os.path.isabs(thumb_path):
                fail(f"results.jsonl: thumbnail_path is a local absolute path: {thumb_path}")
            full = os.path.join(ROOT, thumb_path)
            if not os.path.isfile(full):
                fail(f"results.jsonl: thumbnail_path does not exist on disk: {thumb_path}")

    stats["platform_counts"] = platform_counts
    stats["mapping_confidence_counts"] = confidence_counts
    stats["broken_images"] = broken
    stats["duplicate_image_paths"] = len(dup_paths)
    stats["duplicate_query_platform_rank"] = len(dup_triples)
    stats["hash_mismatches"] = hash_mismatches

    if dup_paths:
        warn(f"results.jsonl: {len(dup_paths)} duplicate image_path value(s) across records: {dup_paths[:5]}")


def check_gallery_html():
    gallery_path = os.path.join(DATA68, "gallery", "index.html")
    if not os.path.isfile(gallery_path):
        fail("data/68-query/gallery/index.html: missing")
        return
    with open(gallery_path, encoding="utf-8") as f:
        html = f.read()

    external_patterns = [
        r'src=["\']https?://', r'href=["\']https?://(?!.*creativecommons)',
        r'<script[^>]+src=["\']https?://', r'@import\s+url\(["\']?https?://',
        r'fonts\.googleapis\.com', r'cdn\.',
    ]
    for pat in external_patterns:
        m = re.search(pat, html, re.IGNORECASE)
        if m:
            fail(f"data/68-query/gallery/index.html: external reference found matching /{pat}/: {m.group(0)[:80]!r}")

    m = re.search(r"const RECORDS = (\[.*?\]);", html, re.S)
    if not m:
        fail("data/68-query/gallery/index.html: could not find embedded RECORDS data array")
        return
    try:
        records = json.loads(m.group(1))
    except json.JSONDecodeError as e:
        fail(f"data/68-query/gallery/index.html: embedded RECORDS JSON invalid ({e})")
        return

    stats["gallery_records"] = len(records)
    gallery_dir = os.path.dirname(gallery_path)
    missing_refs = 0
    for rec in records:
        for key in ("full", "thumb"):
            p = rec.get(key)
            if not p:
                continue
            resolved = os.path.normpath(os.path.join(gallery_dir, p))
            if not os.path.isfile(resolved):
                missing_refs += 1
                fail(f"gallery/index.html: broken reference {key}={p!r} for {rec.get('query_id')}/{rec.get('platform')}")
    stats["gallery_broken_refs"] = missing_refs

    scan_text_for_sensitive(gallery_path, html)


def check_326query_images():
    """326-query screenshot evidence: google-images/ and curify/, each 326 real screenshots.

    Added 2026-08-03. Row-count/referential-integrity/duplicate/orphan checks for the two
    manifests live in scripts/validate_data.py (matching that script's CSV/schema focus); this
    function does the image-specific work: decodability, actual-format-vs-extension match,
    dimension recording, and gallery HTML reference/external-script checks -- the same class of
    check check_68query_images()/check_gallery_html() do for the 68-query image set above.
    """
    for platform, rel_dir, expected_dims in (
        ("google-images", os.path.join(DATA326, "google-images"), (1440, 1000)),
        ("curify", os.path.join(DATA326, "curify"), (1440, 900)),
    ):
        manifest_path = os.path.join(rel_dir, "manifest.csv")
        gallery_path = os.path.join(rel_dir, "gallery.html")
        if not os.path.isfile(manifest_path):
            fail(f"data/326-query/{platform}/manifest.csv: missing")
            continue

        with open(manifest_path, encoding="utf-8") as f:
            manifest_rows = list(csv.DictReader(f))

        decoded = 0
        broken = 0
        wrong_format = 0
        wrong_dims = 0
        dim_counts = {}
        for r in manifest_rows:
            p = r.get("screenshot_path")
            if not p or os.path.isabs(p):
                continue
            full = os.path.join(rel_dir, p)
            if not os.path.isfile(full):
                continue  # already reported as missing by validate_data.py
            try:
                from PIL import Image
                with Image.open(full) as im:
                    im.verify()
                with Image.open(full) as im:
                    im.load()
                    fmt = im.format
                    size = im.size
                decoded += 1
                if fmt != "JPEG":
                    wrong_format += 1
                    fail(f"data/326-query/{platform}/{p}: actual format is {fmt}, not JPEG "
                         f"(filename has a .jpg-shaped extension, so the real format must match)")
                if size != expected_dims:
                    wrong_dims += 1
                    fail(f"data/326-query/{platform}/{p}: dimensions {size} do not match expected "
                         f"{expected_dims}")
                dim_counts[size] = dim_counts.get(size, 0) + 1
            except ImportError:
                pass  # Pillow not installed -- skip decode/format/dim checks, same fallback as 68-query
            except Exception as e:
                broken += 1
                fail(f"data/326-query/{platform}/{p}: image failed to decode ({e})")

        stats[f"326query_{platform.replace('-', '_')}_decoded"] = decoded
        stats[f"326query_{platform.replace('-', '_')}_broken"] = broken
        stats[f"326query_{platform.replace('-', '_')}_wrong_format"] = wrong_format
        stats[f"326query_{platform.replace('-', '_')}_wrong_dims"] = wrong_dims
        stats[f"326query_{platform.replace('-', '_')}_dim_counts"] = {str(k): v for k, v in dim_counts.items()}

        if not os.path.isfile(gallery_path):
            fail(f"data/326-query/{platform}/gallery.html: missing")
            continue
        with open(gallery_path, encoding="utf-8") as f:
            gallery_html = f.read()

        external_patterns = [
            r'src=["\']https?://', r'href=["\']https?://(?!.*creativecommons)',
            r'<script[^>]+src=["\']https?://', r'@import\s+url\(["\']?https?://',
            r'fonts\.googleapis\.com', r'cdn\.',
        ]
        for pat in external_patterns:
            m = re.search(pat, gallery_html, re.IGNORECASE)
            if m:
                fail(f"data/326-query/{platform}/gallery.html: external reference found matching "
                     f"/{pat}/: {m.group(0)[:80]!r}")

        img_srcs = re.findall(r'<img[^>]+src=["\']([^"\']+)["\']', gallery_html)
        missing_refs = 0
        for src in img_srcs:
            resolved = os.path.normpath(os.path.join(rel_dir, src))
            if not os.path.isfile(resolved):
                missing_refs += 1
                fail(f"data/326-query/{platform}/gallery.html: broken image reference {src!r}")
        stats[f"326query_{platform.replace('-', '_')}_gallery_img_tags"] = len(img_srcs)
        stats[f"326query_{platform.replace('-', '_')}_gallery_broken_refs"] = missing_refs

        scan_text_for_sensitive(gallery_path, gallery_html)


def check_repo_wide_sensitive_and_external():
    exts = (".md", ".csv", ".json", ".jsonl", ".html", ".py")
    skip_dirs = {".git", "node_modules", "__pycache__"}
    for dirpath, dirnames, filenames in os.walk(ROOT):
        dirnames[:] = [d for d in dirnames if d not in skip_dirs]
        for fn in filenames:
            if not fn.endswith(exts):
                continue
            full = os.path.join(dirpath, fn)
            rel = os.path.relpath(full, ROOT)
            if rel.endswith("gallery/index.html"):
                continue  # already scanned in detail above
            try:
                with open(full, encoding="utf-8") as f:
                    text = f.read()
            except UnicodeDecodeError:
                fail(f"{rel}: not valid UTF-8")
                continue
            scan_text_for_sensitive(rel, text)


def main():
    check_68query_images()
    check_gallery_html()
    check_326query_images()
    check_repo_wide_sensitive_and_external()

    # 68/326 query counts, for the summary block
    for name, path, expected in (("68-query", os.path.join(DATA68, "queries.csv"), 68),
                                  ("326-query", os.path.join(DATA326, "queries.csv"), 326)):
        if os.path.isfile(path):
            with open(path, encoding="utf-8") as f:
                n = sum(1 for _ in csv.DictReader(f))
            stats[f"{name}_count"] = n
            if n != expected:
                fail(f"{path}: expected {expected} rows, found {n}")

    print("=" * 70)
    print("EXTENDED VALIDATION REPORT (scripts/validate_benchmark.py)")
    print("=" * 70)
    print(json.dumps(stats, indent=2, ensure_ascii=False))
    if warnings:
        print(f"\n{len(warnings)} warning(s):")
        for w in warnings:
            print(f"  [WARN] {w}")
    if failures:
        print(f"\n{len(failures)} failure(s):")
        for f_ in failures:
            print(f"  [FAIL] {f_}")
        print("\nOVERALL: FAIL")
        return 1
    print("\nOVERALL: PASS -- all extended checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
