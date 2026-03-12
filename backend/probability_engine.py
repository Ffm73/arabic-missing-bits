# Author: Faisal Almuhaysh
# Implementation: Written by author

import math

ALPHA = 0.5  # smoothing parameter


def normalize(probs):
    total = sum(probs)
    if total == 0:
        return [1.0 / len(probs)] * len(probs)
    result = []
    for p in probs:
        result.append(p / total)
    return result


def mle_from_counts(counts):
    # P_MLE(x) = count(x) / N
    total = sum(counts)
    if total == 0:
        return [1.0 / len(counts)] * len(counts)
    probs = []
    for c in counts:
        probs.append(c / total)
    return probs


def smooth_counts(counts, alpha=ALPHA):
    # laplace smoothing: P(x) = (count + alpha) / (N + alpha * k)
    k = len(counts)
    total = sum(counts) + alpha * k
    result = []
    for c in counts:
        result.append((c + alpha) / total)
    return result


def get_base_probabilities(candidates):
    probs = []
    for c in candidates:
        probs.append(c["base_prob"])
    return normalize(probs)


def bayesian_update(probs, weights):
    # P(reading | evidence) proportional to P(reading) * P(evidence | reading)
    updated = []
    for i in range(len(probs)):
        updated.append(probs[i] * weights[i])
    return normalize(updated)


def top_confidence(probs):
    if len(probs) == 0:
        return 0.0
    return max(probs)


def num_plausible(probs, threshold=0.05):
    count = 0
    for p in probs:
        if p >= threshold:
            count += 1
    return count
