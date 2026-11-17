"""Statistics students implement (M2 judge calibration, M4 paired bootstrap).

Rules: a judge is a classifier -- measure it like one. A higher mean is not
"better" until the paired CI of the difference excludes 0.
Reference values to self-check are in tests/test_lab9_stats.py.
"""

from __future__ import annotations

from collections.abc import Sequence

POS = "FAIL"   # the judge's job is to FIND failures, so FAIL is the positive class


def confusion(human: Sequence[str], judge: Sequence[str]) -> dict[str, int]:
    """tp/fp/fn/tn with FAIL as positive."""
    counts = {"tp": 0, "fp": 0, "fn": 0, "tn": 0}
    outcomes = {
        (POS, POS): "tp",
        ("PASS", POS): "fp",
        (POS, "PASS"): "fn",
        ("PASS", "PASS"): "tn",
    }
    for pair in zip(human, judge, strict=True):
        outcome = outcomes.get(pair)
        if outcome is None:
            raise ValueError("labels must be PASS or FAIL")
        counts[outcome] += 1
    return counts


def precision_recall(human: Sequence[str], judge: Sequence[str]) -> tuple[float, float]:
    counts = confusion(human, judge)
    true_positives = counts["tp"]
    predicted_failures = true_positives + counts["fp"]
    actual_failures = true_positives + counts["fn"]
    precision = true_positives / predicted_failures if predicted_failures else 0.0
    recall = true_positives / actual_failures if actual_failures else 0.0
    return precision, recall


def cohen_kappa(human: Sequence[str], judge: Sequence[str]) -> float:
    """Return (observed - expected) / (1 - expected) agreement."""
    counts = confusion(human, judge)
    n = sum(counts.values())
    if not n:
        raise ValueError("kappa is undefined without labels")

    human_failures = counts["tp"] + counts["fn"]
    judge_failures = counts["tp"] + counts["fp"]
    expected_agreement = (
        human_failures * judge_failures + (n - human_failures) * (n - judge_failures)
    ) / n**2
    if expected_agreement == 1.0:
        raise ValueError("kappa is undefined when chance agreement is 1")

    observed_agreement = (counts["tp"] + counts["tn"]) / n
    return (observed_agreement - expected_agreement) / (1 - expected_agreement)


def rogan_gladen(observed_rate: float, sensitivity: float, specificity: float) -> float:
    """Correct a failure rate for judge error, clipping defined estimates to [0, 1]."""
    denominator = sensitivity + specificity - 1
    if denominator == 0:
        return float("nan")
    corrected = (observed_rate + specificity - 1) / denominator
    return min(max(corrected, 0.0), 1.0)


def paired_bootstrap(a: Sequence[float], b: Sequence[float], *, n_resamples: int = 1000,
                     rng: int = 2027, confidence: float = 0.95) -> tuple[float, float, float]:
    """a[i], b[i] = per-item mean over seeds, SAME items, SAME order.
    Return (mean(a)-mean(b), lo, hi) with scipy.stats.bootstrap(paired=True, method="percentile",
    rng=numpy.random.default_rng(rng)). If a == b everywhere return (0.0, 0.0, 0.0)."""
    import numpy as np
    from scipy.stats import bootstrap

    pr = np.asarray(a, dtype=float)
    baseline = np.asarray(b, dtype=float)
    if pr.ndim != 1 or pr.shape != baseline.shape or pr.size == 0:
        raise ValueError("paired bootstrap requires equally sized, non-empty vectors")
    if not (np.isfinite(pr).all() and np.isfinite(baseline).all()):
        raise ValueError("paired bootstrap requires finite scores")

    if np.array_equal(pr, baseline):
        return 0.0, 0.0, 0.0

    def mean_difference(current, reference, axis=-1):
        return np.mean(current - reference, axis=axis)

    delta = float(mean_difference(pr, baseline))
    if pr.size == 1:
        return delta, delta, delta

    result = bootstrap(
        (pr, baseline),
        mean_difference,
        paired=True,
        method="percentile",
        n_resamples=n_resamples,
        confidence_level=confidence,
        rng=np.random.default_rng(rng),
    )
    interval = result.confidence_interval
    return delta, float(interval.low), float(interval.high)


def pass_at_k(n: int, c: int, k: int) -> float:
    """Probability that AT LEAST ONE of k trials drawn from n (c of them passing) passes.
    Unbiased estimator (Chen et al. 2021): 1 - C(n-c, k) / C(n, k). Raise ValueError if k > n."""
    # TODO M6
    raise NotImplementedError


def pass_hat_k(n: int, c: int, k: int) -> float:
    """pass^k (tau-bench, Yao et al. 2024): probability that ALL k trials drawn from n pass.
    Unbiased estimator: C(c, k) / C(n, k). Raise ValueError if k > n.
    pass^k <= pass@1 <= pass@k; a reliable agent keeps pass^k close to pass@1."""
    # TODO M6
    raise NotImplementedError
