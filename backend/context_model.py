# Author: Faisal Almuhaysh
# Implementation: Written by author

from probability_engine import bayesian_update


def get_context_weights(candidates, context):
    weight_map = context.get("weights", {})
    weights = []
    for c in candidates:
        w = weight_map.get(c["id"], 1.0)
        weights.append(w)
    return weights


def apply_context(probs, candidates, context):
    # P(reading | context) proportional to P(reading) * P(context | reading)
    if context is None:
        return probs
    weights = get_context_weights(candidates, context)
    return bayesian_update(probs, weights)


def get_context_explanation(probs_before, probs_after, candidates, context):
    top_i = 0
    top_p = 0.0
    for i in range(len(probs_after)):
        if probs_after[i] > top_p:
            top_p = probs_after[i]
            top_i = i

    top_cand = candidates[top_i]
    pct = round(top_p * 100)

    expl = context.get("explanation", "")
    if expl:
        return f"Conditional update: '{top_cand['gloss']}' becomes the dominant reading at {pct}%. {expl}"
    return f"Context makes '{top_cand['gloss']}' the most likely reading at {pct}%."
