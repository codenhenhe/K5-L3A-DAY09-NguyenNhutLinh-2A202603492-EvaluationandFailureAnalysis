"""CI gate: compare a PR eval report with the main-branch baseline using the metric spec.

    python -m lab9.gate --pr reports/eval_workflow.json --baseline reports/baseline_v1.json

exit 0 = merge, exit 1 = blocked. Safety metrics: max 0, no averaging away.
Capability metrics: meet the floor AND the paired CI of (PR - main) is not entirely below 0.
Thresholds may only get stricter on the same eval-set version (ratchet).
"""

from __future__ import annotations

import argparse
import json
from math import isfinite
from pathlib import Path

from lab8.console import utf8_stdio
from lab9 import stats
from lab9.eval import SPEC, aggregate, load_spec, per_item
from lab9.graders import GRADERS


def _finite(value: object) -> bool:
    return type(value) in (int, float) and isfinite(value)


def _report_integrity(report: dict, spec: dict, label: str) -> tuple[dict, list[str]]:
    problems = []
    if report.get("evaluator_failures"):
        problems.append(f"{label} has evaluator failures")
    metrics = report.get("metrics", {})
    for metric_id, value in metrics.items():
        if not _finite(value):
            problems.append(f"{label} metric {metric_id} is not finite")

    rows = report.get("rows", [])
    manifest = report["manifest"]
    item_count, seeds = manifest.get("items"), manifest.get("seeds", [])
    if (type(item_count) is not int or item_count <= 0 or not seeds
            or any(type(seed) is not int for seed in seeds) or len(set(seeds)) != len(seeds)):
        return {}, [*problems, f"{label} has an invalid item count or seed list"]
    if len(rows) != item_count * len(seeds):
        problems.append(f"{label} row count differs from manifest items × seeds")

    declared_seeds = set(seeds)
    row_metrics = [m["id"] for m in spec["metrics"] if m["id"] in GRADERS]
    row_slices = {}
    items = set()
    for row in rows:
        item, seed = row.get("item_id"), row.get("seed")
        if not isinstance(item, str) or not item or type(seed) is not int or seed not in declared_seeds:
            return row_slices, [*problems, f"{label} contains an invalid item or seed"]
        if (item, seed) in row_slices:
            return row_slices, [*problems, f"{label} contains a duplicate row for {item}@{seed}"]
        slices = row.get("slices", [])
        if not isinstance(slices, list) or any(not isinstance(tag, str) for tag in slices):
            return row_slices, [*problems, f"{label} has invalid slice tags for {item}@{seed}"]
        row_slices[item, seed] = frozenset(slices)
        items.add(item)
        for metric_id in row_metrics:
            if type(row.get(metric_id)) is not bool:
                return row_slices, [*problems, f"{label} lacks a boolean {metric_id} score for {item}@{seed}"]
        if "cost_per_success" in metrics and not _finite(row.get("cost")):
            return row_slices, [*problems, f"{label} has an invalid cost for {item}@{seed}"]

    if len(items) != item_count:
        problems.append(f"{label} item count differs from manifest")
    if not problems:
        # The aggregation helper always expects costs, even in a minimal test report.
        scored_rows = [{"cost": 0.0, **row} for row in rows] if "cost_per_success" not in metrics else rows
        actual = aggregate(scored_rows, row_metrics, k_values=spec.get("pass_k", []))
        for metric_id in sorted(actual.keys() & metrics.keys()):
            if actual[metric_id] != metrics[metric_id]:
                problems.append(f"{label} metric {metric_id} disagrees with its rows")
    return row_slices, problems


def _looser(current: dict, previous: dict) -> bool:
    if previous.get("no_significant_drop") and not current.get("no_significant_drop"):
        return True
    if "min" in previous and ("min" not in current or current["min"] < previous["min"]):
        return True
    return any(key in previous and (key not in current or current[key] > previous[key])
               for key in ("max", "max_increase"))


def _ratchet(spec: dict, base_spec: dict) -> list[str]:
    if spec.get("eval_set_version") != base_spec.get("eval_set_version"):
        return []
    problems = []
    metrics = {m["id"]: m for m in spec["metrics"]}
    for old in base_spec["metrics"]:
        metric_id = old["id"]
        new = metrics.get(metric_id)
        if (new is None or (old.get("blocking") and not new.get("blocking"))
                or _looser(new.get("threshold", {}), old.get("threshold", {}))):
            problems.append(f"ratchet: metric {metric_id} was removed or loosened")
    slices = {(s["name"], s["metric"]): s for s in spec.get("slices", [])}
    for old in base_spec.get("slices", []):
        name, metric_id = old["name"], old["metric"]
        new = slices.get((name, metric_id))
        if new is None or (old.get("blocking") and not new.get("blocking")) or _looser(new, old):
            problems.append(f"ratchet: slice {name}/{metric_id} was removed or loosened")
    return problems


def integrity_check(pr: dict, base: dict, spec: dict, base_spec: dict | None = None) -> list[str]:
    """M7 (Expert): refuse to compare reports that cannot be trusted. Return a list of problems
    (empty = trustworthy). A gate that passes a broken report is worse than no gate.
    Must catch at least:
      - any metric value in pr["metrics"] that is NaN or inf
      - len(pr["rows"]) != manifest items x len(manifest seeds)   (dropped / duplicated rows)
      - the (item_id, seed) set of PR differs from the baseline's (cherry-picked seeds/items)
      - pr["evaluator_failures"] non-empty, or a row whose value for a graded spec metric is
        None (a crashed grader silently scores as "missing" and drops out of the mean)
      - base_spec given and a threshold in spec is LOOSER than in base_spec for the same
        eval-set version (ratchet: max may not rise, min may not fall, a blocking metric may
        not become non-blocking, a metric may not disappear; the same for spec["slices"],
        including dropping no_significant_drop)
      - an item's slice tags in PR rows differ from the baseline's (relabelling an item out of a
        slice hides its regression from the slice gate)"""
    current_rows, problems = _report_integrity(pr, spec, "PR")
    base_rows, baseline_problems = _report_integrity(base, base_spec or spec, "baseline")
    problems.extend(baseline_problems)
    if current_rows.keys() != base_rows.keys():
        problems.append("PR and baseline have different (item, seed) pairs")
    elif current_rows != base_rows:
        problems.append("PR slice tags differ from baseline")
    if base_spec is not None:
        problems.extend(_ratchet(spec, base_spec))
    return problems


def _paired_interval(current: dict, baseline: dict, bootstrap: dict) -> tuple[float, float, float]:
    keys = sorted(current)
    return stats.paired_bootstrap(
        [current[key] for key in keys],
        [baseline[key] for key in keys],
        n_resamples=bootstrap.get("n_resamples", 1000),
        rng=bootstrap.get("rng", 2027),
        confidence=bootstrap.get("confidence", 0.95),
    )


def slice_check(pr: dict, base: dict, spec: dict) -> tuple[list[str], list[str]]:
    """M5 (Advanced): an average can hide a regression on a small, important slice.
    For each entry of spec["slices"] ({"name", "metric", "min"?, "no_significant_drop"?, "blocking"}):
      - value = mean of per_item(pr, metric, slice_name=name)
      - fail if below "min", or if no_significant_drop and the paired CI over the slice's items
        lies entirely below 0
    Return (blocked ids like "slice:money_movement/pass_rate", report lines)."""
    blocked, lines = [], []
    for rule in spec.get("slices", []):
        name, metric_id = rule["name"], rule["metric"]
        slice_id = f"slice:{name}/{metric_id}"
        current = per_item(pr, metric_id, slice_name=name)
        baseline = per_item(base, metric_id, slice_name=name)
        if not current or (rule.get("no_significant_drop") and current.keys() != baseline.keys()):
            failed, detail = True, "missing comparable slice scores"
        else:
            value = sum(current.values()) / len(current)
            failed = "min" in rule and value < rule["min"]
            detail = f"{value:.4f}"
            if rule.get("no_significant_drop"):
                delta, lo, hi = _paired_interval(current, baseline, spec.get("bootstrap", {}))
                failed |= hi < 0
                detail += f" Δ {delta:+.3f} CI [{lo:+.3f}, {hi:+.3f}]"
        verdict = "ok"
        if failed:
            verdict = "BLOCK" if rule.get("blocking") else "warn"
            if rule.get("blocking"):
                blocked.append(slice_id)
        lines.append(f"  {slice_id:<37} {detail} {verdict}")
    return blocked, lines


def check(pr: dict, base: dict, spec: dict, base_spec: dict | None = None) -> tuple[list[str], list[str]]:
    if pr["manifest"]["eval_set_sha"] != base["manifest"]["eval_set_sha"]:
        return ["eval_set_sha"], ["  EVAL SET differs from the baseline's: re-run the baseline on the same eval set"]
    problems = integrity_check(pr, base, spec, base_spec)
    if problems:
        return ["integrity"], [f"  INTEGRITY {p}" for p in problems]
    blocked, lines = [], []
    bs = spec.get("bootstrap", {})
    for m in spec["metrics"]:
        mid, th, val = m["id"], m.get("threshold", {}), pr["metrics"].get(m["id"])
        verdict, note = "ok", ""
        if val is None:
            verdict = "missing"
        elif "max" in th and val > th["max"]:
            verdict = "fail"
        elif "min" in th and val < th["min"]:
            verdict = "fail"
        elif "max_increase" in th and base["metrics"].get(mid):
            if val > base["metrics"][mid] * (1 + th["max_increase"]):
                verdict = "fail"
        if th.get("no_significant_drop") and val is not None:
            a, b = per_item(pr, mid), per_item(base, mid)
            if not a or a.keys() != b.keys():
                verdict, note = "missing", "missing comparable item scores"
            else:
                d, lo, hi = _paired_interval(a, b, bs)
                note = f"Δ {d:+.3f} CI [{lo:+.3f}, {hi:+.3f}]"
                if hi < 0:
                    verdict = "fail"
        if verdict != "ok" and m.get("blocking"):
            blocked.append(mid)
        label = {"ok": "ok", "missing": "MISSING"}.get(verdict, "BLOCK" if m.get("blocking") else "warn")
        lines.append(f"  {mid:<22} {val!s:<8} {json.dumps(th):<40} {note:<28} {label}")
    if spec.get("slices"):
        sb, sl = slice_check(pr, base, spec)
        blocked += sb
        lines += sl
    return blocked, lines


def main(argv: list[str] | None = None) -> int:
    utf8_stdio()
    ap = argparse.ArgumentParser(prog="lab9.gate")
    ap.add_argument("--pr", required=True)
    ap.add_argument("--baseline", required=True)
    ap.add_argument("--spec", default=str(SPEC))
    ap.add_argument("--base-spec", help="metric spec on main, for the ratchet check (M7)")
    args = ap.parse_args(argv)
    pr = json.loads(Path(args.pr).read_text(encoding="utf-8"))
    base = json.loads(Path(args.baseline).read_text(encoding="utf-8"))
    base_spec = load_spec(Path(args.base_spec)) if args.base_spec else None
    blocked, lines = check(pr, base, load_spec(Path(args.spec)), base_spec)
    print(f"gate: PR {pr['run_id']} vs main {base['run_id']} · eval set {pr['manifest']['eval_set_sha']}")
    print("\n".join(lines))
    if blocked:
        print(f"exit 1 — blocked: {', '.join(blocked)}")
        return 1
    print("exit 0 — merge")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
