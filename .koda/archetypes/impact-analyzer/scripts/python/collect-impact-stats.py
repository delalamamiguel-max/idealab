#!/usr/bin/env python3
"""Collect quantitative impact metrics for the impact-analysis archetype.

This script scans a workspace subtree for files referencing a target token, groups
matches by file category (SQL, orchestration, etc.), and produces derived metrics
that downstream archetypes can use when estimating effort.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
import time
from collections import defaultdict
from fnmatch import fnmatch
from typing import Any, Dict, Iterable, List, Tuple

try:
    import yaml  # type: ignore
except ImportError as exc:  # pragma: no cover - dependency issue handled upstream
    raise SystemExit("pyyaml is required to run collect-impact-stats.py") from exc


DEFAULT_ENV_CONFIG = (
    "templates/env-config.yaml"
)
DEFAULT_ESTIMATION_CONFIG = (
    "templates/estimation-config.json"
)
DEFAULT_OUTPUT_PATH = "cache/impact_scope_stats.json"


def load_yaml(path: str) -> Dict:
    with open(path, "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def load_json(path: str) -> Dict:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def build_pattern_index(file_patterns: Dict[str, Iterable[str]]) -> List[Tuple[str, str]]:
    index: List[Tuple[str, str]] = []
    for category, patterns in file_patterns.items():
        for pattern in patterns or []:
            index.append((category, pattern))
    return index


def categorize_file(filename: str, pattern_index: List[Tuple[str, str]], fallback: str = "other") -> str:
    basename = os.path.basename(filename)
    for category, pattern in pattern_index:
        if fnmatch(basename, pattern):
            return category
    return fallback


def iter_files(root: str, ignored_dirs: Iterable[str]) -> Iterable[str]:
    ignored = {os.path.normpath(d) for d in ignored_dirs}
    for dirpath, dirnames, filenames in os.walk(root):
        # prune ignored directories in-place
        dirnames[:] = [d for d in dirnames if os.path.join(dirpath, d) not in ignored and d not in ignored]
        for name in filenames:
            yield os.path.join(dirpath, name)


def count_occurrences(path: str, target: str, case_sensitive: bool = False, max_bytes: int = 5 * 1024 * 1024) -> int:
    try:
        with open(path, "r", encoding="utf-8", errors="ignore") as fh:
            data = fh.read(max_bytes + 1)
    except (OSError, UnicodeDecodeError):  # binary or unreadable
        return 0

    if len(data) > max_bytes:
        data = data[:max_bytes]

    if case_sensitive:
        return data.count(target)

    return data.lower().count(target.lower())


def determine_complexity(total_files: int, thresholds: Dict[str, int]) -> str:
    ordered = sorted(thresholds.items(), key=lambda item: item[1])
    for label, limit in ordered:
        if total_files <= limit:
            return label
    return ordered[-1][0] if ordered else "Unknown"


def choose_phase_model(layer_count: int, total_files: int, complexity: str, thresholds: Dict[str, int]) -> str:
    if layer_count >= 3 and (complexity in {"Large", "X-Large"} or total_files >= thresholds.get("Large", 75)):
        return "program"
    if layer_count >= 2:
        return "multi_layer"
    return "single_layer"


def main() -> int:
    parser = argparse.ArgumentParser(description="Collect impact statistics for estimation")
    parser.add_argument("--root", required=True, help="Root directory to scan")
    parser.add_argument("--target", required=True, help="Target string (table/column name) to search for")
    parser.add_argument("--env-config", default=DEFAULT_ENV_CONFIG, help="Path to env config YAML")
    parser.add_argument("--estimation-config", default=DEFAULT_ESTIMATION_CONFIG, help="Path to estimation config JSON")
    parser.add_argument("--output", default=DEFAULT_OUTPUT_PATH, help="File to write JSON metrics to")
    parser.add_argument("--case-sensitive", action="store_true", help="Enable case sensitive matching")
    args = parser.parse_args()

    if not os.path.isdir(args.root):
        raise SystemExit(f"Root directory not found: {args.root}")
    env_config = load_yaml(args.env_config)
    estimation_config = load_json(args.estimation_config)

    file_patterns = env_config.get("file_patterns", {})
    ignored_dirs = env_config.get("ignored_directories", [])
    pattern_index = build_pattern_index(file_patterns)

    category_counts = defaultdict(lambda: {"files": 0, "occurrences": 0})
    matched_files: Dict[str, Dict[str, Any]] = {}

    total_files_scanned = 0
    total_files_matched = 0
    total_occurrences = 0

    for filepath in iter_files(args.root, ignored_dirs):
        total_files_scanned += 1
        count = count_occurrences(filepath, args.target, case_sensitive=args.case_sensitive)
        if count == 0:
            continue

        category = categorize_file(filepath, pattern_index)
        category_counts[category]["files"] += 1
        category_counts[category]["occurrences"] += count
        matched_files[filepath] = {"category": category, "occurrences": count}
        total_files_matched += 1
        total_occurrences += count

    complexity_thresholds = estimation_config.get("complexity_thresholds", {})
    complexity_bucket = determine_complexity(total_files_matched, complexity_thresholds)

    layer_mapping = estimation_config.get("layer_mapping", {})
    layers_impacted = sorted({layer_mapping.get(category, "other") for category, meta in category_counts.items() if meta["files"] > 0})
    phase_model = choose_phase_model(len(layers_impacted), total_files_matched, complexity_bucket, complexity_thresholds)

    category_weights = estimation_config.get("category_weights", {})
    weighted_hours = 0.0
    for category, meta in category_counts.items():
        weight = category_weights.get(category, {"hours_per_file": 1.5, "hours_per_occurrence": 0.05})
        category_hours = meta["files"] * weight.get("hours_per_file", 1.5) + meta["occurrences"] * weight.get("hours_per_occurrence", 0.05)
        meta["weighted_hours"] = round(category_hours, 2)
        weighted_hours += category_hours

    phase_baseline = estimation_config.get("phase_models", {}).get(phase_model, {})
    buffer_defaults = estimation_config.get("buffer_defaults", {})

    result = {
        "target": args.target,
        "root": os.path.abspath(args.root),
        "generated_at": int(time.time()),
        "case_sensitive": args.case_sensitive,
        "total_files_scanned": total_files_scanned,
        "total_files_matched": total_files_matched,
        "total_occurrences": total_occurrences,
        "category_breakdown": category_counts,
        "layers_impacted": layers_impacted,
        "complexity_bucket": complexity_bucket,
        "phase_model": phase_model,
        "phase_baseline_hours": phase_baseline,
        "buffer_recommendation": buffer_defaults.get(phase_model),
        "weighted_file_hours": round(weighted_hours, 2),
        "matched_files": matched_files,
        "env_config": args.env_config,
        "estimation_config": args.estimation_config,
    }

    os.makedirs(os.path.dirname(args.output), exist_ok=True)
    with open(args.output, "w", encoding="utf-8") as fh:
        json.dump(result, fh, indent=2)

    json.dump(result, sys.stdout, indent=2)
    print()  # newline
    return 0


if __name__ == "__main__":
    sys.exit(main())
