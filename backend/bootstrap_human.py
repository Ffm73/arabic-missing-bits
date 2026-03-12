# Author: Faisal Almuhaysh
# Implementation: Written by author

import random


def expand_counts_to_samples(count_dict):
    # list of labels, one per respondent
    out = []
    for label, count in count_dict.items():
        for _ in range(count):
            out.append(label)
    return out


def percentile(values, p):
    # p in 0..100
    if not values:
        return 0.0
    v = sorted(values)
    n = len(v)
    idx = p / 100.0 * (n - 1)
    i = int(idx)
    if i >= n - 1:
        return v[-1]
    frac = idx - i
    return v[i] * (1 - frac) + v[i + 1] * frac


def bootstrap_human_distribution(samples, num_bootstrap=1000, low_p=5, high_p=95, all_readings=None):
    n = len(samples)
    if n == 0:
        return {}
    readings = list(set(samples)) if all_readings is None else list(all_readings)
    by_reading = {}
    for r in readings:
        by_reading[r] = []

    for _ in range(num_bootstrap):
        resampled = [random.choice(samples) for _ in range(n)]
        counts = {}
        for r in readings:
            counts[r] = 0
        for label in resampled:
            counts[label] = counts.get(label, 0) + 1
        for r in readings:
            by_reading[r].append(counts[r] / n)

    result = {}
    for r in readings:
        vals = by_reading[r]
        result[r] = {
            "mean": round(sum(vals) / len(vals), 4),
            "low": round(percentile(vals, low_p), 4),
            "high": round(percentile(vals, high_p), 4),
        }
    return result


def compute_bootstrap_stats(guesses_dict):
    total = sum(guesses_dict.values())
    if total == 0:
        return {}, {}
    human_distribution = {}
    for label, count in guesses_dict.items():
        human_distribution[label] = round(count / total, 4)
    samples = expand_counts_to_samples(guesses_dict)
    bootstrap = bootstrap_human_distribution(
        samples, num_bootstrap=1000, low_p=5, high_p=95, all_readings=guesses_dict.keys()
    )
    for label in guesses_dict:
        if label not in bootstrap:
            bootstrap[label] = {"mean": 0.0, "low": 0.0, "high": 0.0}
    return human_distribution, bootstrap
