#!/usr/bin/env python3
"""Deterministic validator for the Curify Visual Search Benchmark public data.

Runs with: python3 scripts/validate_data.py
Exit code 0 only if every mandatory check passes.

Uses only the Python standard library.
"""
import csv
import json
import os
import re
import sys
import hashlib

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

failures = []
warnings = []


def fail(msg):
    failures.append(msg)


def warn(msg):
    warnings.append(msg)


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        h.update(f.read())
    return h.hexdigest()


def read_csv_rows(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def check_valid_utf8(path):
    try:
        with open(path, "rb") as f:
            f.read().decode("utf-8")
        return True
    except UnicodeDecodeError:
        fail(f"{path}: not valid UTF-8")
        return False


SENSITIVE_PATTERNS = [
    (r"/Users/[^\"'\s,]*", "local absolute path (/Users/)"),
    (r"/home/[^\"'\s,]*", "local absolute path (/home/)"),
    (r"file://", "file:// URL"),
    (r"\blocalhost\b", "localhost reference"),
    (r"127\.0\.0\.1", "loopback IP"),
    (r"\bAPI_KEY\b", "API_KEY-shaped string"),
    (r"\bSECRET\b", "SECRET-shaped string"),
    (r"\bPASSWORD\b", "PASSWORD-shaped string"),
    (r"\bAUTHORIZATION\b", "AUTHORIZATION-shaped string"),
    (r"\bBEARER\b", "BEARER-shaped string"),
    (r"\bCOOKIE\b", "COOKIE-shaped string"),
    (r"\bSESSION\b", "SESSION-shaped string"),
    (r"PRIVATE KEY", "PRIVATE KEY string"),
    (r"ghp_[A-Za-z0-9]{10,}", "GitHub personal access token"),
    (r"github_pat_[A-Za-z0-9_]{10,}", "GitHub fine-grained PAT"),
    (r"(?<![A-Za-z0-9_-])sk-[A-Za-z0-9]{10,}", "sk- style API key"),
]
SENSITIVE_RE = [(re.compile(p, re.IGNORECASE if "PRIVATE KEY" not in p and "ghp_" not in p and "sk-" not in p else 0), label) for p, label in SENSITIVE_PATTERNS]


def scan_sensitive(path):
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        text = f.read()
    for regex, label in SENSITIVE_RE:
        m = regex.search(text)
        if m:
            fail(f"{path}: possible {label} found: {m.group(0)[:60]!r}")


def check_no_forbidden_files():
    forbidden_names = {".DS_Store"}
    forbidden_dirs = {"__pycache__", "node_modules"}
    forbidden_suffixes = (".pyc", ".swp", ".swo", ".lock~")
    for dirpath, dirnames, filenames in os.walk(ROOT):
        if ".git" in dirpath.split(os.sep):
            continue
        dirnames[:] = [d for d in dirnames if d not in forbidden_dirs and d != ".git"]
        for d in list(dirnames):
            if d in forbidden_dirs:
                fail(f"{os.path.join(dirpath, d)}: forbidden directory present")
        for fn in filenames:
            full = os.path.join(dirpath, fn)
            if fn in forbidden_names:
                fail(f"{full}: forbidden file present")
            if fn.startswith(".~") or fn.startswith("~$"):
                fail(f"{full}: temporary/lock editor file present")
            if fn.endswith(forbidden_suffixes):
                fail(f"{full}: forbidden temp/compiled file present")
            if fn.startswith(".") and fn not in {".gitignore"}:
                warn(f"{full}: hidden file present (review manually)")


REQUIRED_FILES = [
    "README.md",
    "data/README.md",
    "LICENSE",
    "CITATION.cff",
    "METHODOLOGY.md",
    "SOURCE_AUDIT.md",
    "scripts/validate_data.py",
    "data/68-query/README.md",
    "data/68-query/queries.csv",
    "data/68-query/automated_relevance_labels.csv",
    "data/68-query/schema.json",
    "data/68-query/provenance.json",
    "data/326-query/README.md",
    "data/326-query/queries.csv",
    "data/326-query/evaluations.csv",
    "data/326-query/schema.json",
    "data/326-query/provenance.json",
]


def check_required_files():
    for rel in REQUIRED_FILES:
        full = os.path.join(ROOT, rel)
        if not os.path.isfile(full):
            fail(f"required file missing: {rel}")


def check_json_parses(rel):
    full = os.path.join(ROOT, rel)
    if not os.path.isfile(full):
        return None
    check_valid_utf8(full)
    try:
        with open(full, encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        fail(f"{rel}: invalid JSON ({e})")
        return None


def check_csv_parses(rel):
    full = os.path.join(ROOT, rel)
    if not os.path.isfile(full):
        return None
    check_valid_utf8(full)
    try:
        return read_csv_rows(full)
    except Exception as e:
        fail(f"{rel}: failed to parse as CSV ({e})")
        return None


def normalize_query(q):
    return re.sub(r"\s+", " ", q.strip().lower())


def check_query_file(rel, expected_count):
    rows = check_csv_parses(rel)
    if rows is None:
        return None
    if len(rows) != expected_count:
        fail(f"{rel}: expected {expected_count} rows, found {len(rows)}")
    ids = [r.get("query_id", "") for r in rows]
    queries = [r.get("query", "") for r in rows]
    if any(not q.strip() for q in queries):
        fail(f"{rel}: contains an empty query")
    if len(set(ids)) != len(ids):
        fail(f"{rel}: duplicate query_id values found")
    normalized = [normalize_query(q) for q in queries]
    if len(set(normalized)) != len(normalized):
        fail(f"{rel}: duplicate normalized query text found")
    return rows


def check_schema_matches_headers(schema_rel, csv_rel, csv_key):
    schema = check_json_parses(schema_rel)
    rows = None
    full_csv = os.path.join(ROOT, csv_rel)
    if schema is None or not os.path.isfile(full_csv):
        return
    with open(full_csv, newline="", encoding="utf-8") as f:
        reader = csv.reader(f)
        header = next(reader)
    expected_fields = [fdef["name"] for fdef in schema.get(csv_key, {}).get("fields", [])]
    if header != expected_fields:
        fail(f"{csv_rel}: header {header} does not match schema.json {csv_key}.fields {expected_fields}")


def check_provenance_hashes(provenance_rel, data_dir):
    prov = check_json_parses(provenance_rel)
    if prov is None:
        return
    for fname, expected_hash in prov.get("public_file_sha256", {}).items():
        full = os.path.join(ROOT, data_dir, fname)
        if not os.path.isfile(full):
            fail(f"{provenance_rel}: references missing public file {fname}")
            continue
        actual = sha256_of(full)
        if actual != expected_hash:
            fail(f"{data_dir}/{fname}: sha256 {actual} does not match provenance.json recorded hash {expected_hash}")


def main():
    check_required_files()
    check_no_forbidden_files()

    for rel in REQUIRED_FILES:
        full = os.path.join(ROOT, rel)
        if os.path.isfile(full) and (rel.endswith(".csv") or rel.endswith(".json") or rel.endswith(".md")):
            check_valid_utf8(full)
            scan_sensitive(full)

    # ---------------- 68-query ----------------
    q68 = check_query_file("data/68-query/queries.csv", 68)
    labels68 = check_csv_parses("data/68-query/automated_relevance_labels.csv")
    check_schema_matches_headers("data/68-query/schema.json", "data/68-query/queries.csv", "queries.csv")
    check_schema_matches_headers("data/68-query/schema.json", "data/68-query/automated_relevance_labels.csv", "automated_relevance_labels.csv")
    check_provenance_hashes("data/68-query/provenance.json", "data/68-query")

    if q68 is not None and labels68 is not None:
        query_ids_68 = {r["query_id"] for r in q68}
        eval_ids_68 = [r.get("query_id", "") for r in labels68]
        if len(labels68) != 68:
            fail(f"data/68-query/automated_relevance_labels.csv: expected 68 rows, found {len(labels68)}")
        unknown = [i for i in eval_ids_68 if i not in query_ids_68]
        if unknown:
            fail(f"data/68-query/automated_relevance_labels.csv: unexpected query_id(s) not in queries.csv: {unknown[:5]}")
        missing = query_ids_68 - set(eval_ids_68)
        if missing:
            fail(f"data/68-query/automated_relevance_labels.csv: missing evaluation coverage for query_id(s): {sorted(missing)[:5]}")
        allowed_labels_68 = {"PASS", "WARN", "FAIL"}
        bad_labels = {r["claude_relevance_label"] for r in labels68} - allowed_labels_68
        if bad_labels:
            fail(f"data/68-query/automated_relevance_labels.csv: unsupported claude_relevance_label value(s): {bad_labels}")
        expected_label_dist = {"FAIL": 43, "WARN": 25}
        actual_dist = {}
        for r in labels68:
            actual_dist[r["claude_relevance_label"]] = actual_dist.get(r["claude_relevance_label"], 0) + 1
        for label, count in expected_label_dist.items():
            if actual_dist.get(label, 0) != count:
                fail(f"data/68-query/automated_relevance_labels.csv: expected {count} rows labeled {label}, found {actual_dist.get(label, 0)}")
        if "PASS" in actual_dist and actual_dist["PASS"] != 0:
            fail("data/68-query/automated_relevance_labels.csv: expected 0 PASS rows in this snapshot, found some")
        header68 = list(labels68[0].keys()) if labels68 else []
        for forbidden in ("diversity", "actionability", "diversity_score", "actionability_score"):
            if forbidden in header68:
                fail(f"data/68-query/automated_relevance_labels.csv: unsupported fabricated column '{forbidden}' present")

    # ---------------- 326-query ----------------
    q326 = check_query_file("data/326-query/queries.csv", 326)
    evals326 = check_csv_parses("data/326-query/evaluations.csv")
    check_schema_matches_headers("data/326-query/schema.json", "data/326-query/queries.csv", "queries.csv")
    check_schema_matches_headers("data/326-query/schema.json", "data/326-query/evaluations.csv", "evaluations.csv")
    check_provenance_hashes("data/326-query/provenance.json", "data/326-query")

    if q326 is not None:
        lang_dist = {}
        for r in q326:
            lang_dist[r["language"]] = lang_dist.get(r["language"], 0) + 1
        if lang_dist.get("zh") != 163 or lang_dist.get("en") != 163:
            fail(f"data/326-query/queries.csv: expected 163 zh / 163 en, found {lang_dist}")
        scenario_dist = {}
        for r in q326:
            scenario_dist[r["scenario"]] = scenario_dist.get(r["scenario"], 0) + 1
        expected_scenario = {"creative_merch": 82, "brand_business": 82, "marketing_ecommerce": 82, "education": 80}
        if scenario_dist != expected_scenario:
            fail(f"data/326-query/queries.csv: scenario distribution {scenario_dist} does not match expected {expected_scenario}")

    allowed_labels_326 = {"PASS", "PARTIAL", "FAIL", "UNJUDGABLE"}
    if q326 is not None and evals326 is not None:
        query_ids_326 = {r["query_id"] for r in q326}
        variants = {}
        for r in evals326:
            variants.setdefault(r.get("run_variant", ""), []).append(r)
        expected_variants = {"production_baseline_2026-07-21", "candidate_2026-07-22_0e794cd9"}
        if set(variants.keys()) != expected_variants:
            fail(f"data/326-query/evaluations.csv: run_variant values {set(variants.keys())} do not match expected {expected_variants}")
        expected_label_totals = {
            "production_baseline_2026-07-21": {"FAIL": 207, "PARTIAL": 83, "PASS": 24, "UNJUDGABLE": 12},
            "candidate_2026-07-22_0e794cd9": {"FAIL": 195, "PARTIAL": 86, "PASS": 38, "UNJUDGABLE": 7},
        }
        expected_zero_low = {
            "production_baseline_2026-07-21": (23, 19),
            "candidate_2026-07-22_0e794cd9": (20, 18),
        }
        for variant, rows in variants.items():
            if len(rows) != 326:
                fail(f"data/326-query/evaluations.csv: run_variant {variant} has {len(rows)} rows, expected 326")
            ids_in_variant = {r["query_id"] for r in rows}
            unknown = ids_in_variant - query_ids_326
            if unknown:
                fail(f"data/326-query/evaluations.csv: run_variant {variant} has unexpected query_id(s): {list(unknown)[:5]}")
            missing = query_ids_326 - ids_in_variant
            if missing:
                fail(f"data/326-query/evaluations.csv: run_variant {variant} missing coverage for query_id(s): {sorted(missing)[:5]}")
            bad_labels = {r["relevance_label"] for r in rows} - allowed_labels_326
            if bad_labels:
                fail(f"data/326-query/evaluations.csv: run_variant {variant} has unsupported relevance_label value(s): {bad_labels}")
            if variant in expected_label_totals:
                dist = {}
                for r in rows:
                    dist[r["relevance_label"]] = dist.get(r["relevance_label"], 0) + 1
                if dist != expected_label_totals[variant]:
                    fail(f"data/326-query/evaluations.csv: run_variant {variant} label distribution {dist} does not match expected {expected_label_totals[variant]}")
            if variant in expected_zero_low:
                zc = sum(1 for r in rows if r["zero_result"].strip().lower() == "true")
                lc = sum(1 for r in rows if r["low_result"].strip().lower() == "true")
                exp_z, exp_l = expected_zero_low[variant]
                if (zc, lc) != (exp_z, exp_l):
                    fail(f"data/326-query/evaluations.csv: run_variant {variant} zero_result/low_result counts ({zc},{lc}) do not match expected ({exp_z},{exp_l})")

    print("=" * 70)
    print("VALIDATION REPORT")
    print("=" * 70)
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
    print("\nOVERALL: PASS — all mandatory checks passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
