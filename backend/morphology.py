# Author: Faisal Almuhaysh
# Implementation: Written by author

from probability_engine import bayesian_update


def get_morph_weights(candidates):
    weights = []
    for c in candidates:
        w = c.get("morph_weight", 1.0)
        weights.append(w)
    return weights


def apply_morphology(probs, candidates):
    weights = get_morph_weights(candidates)
    return bayesian_update(probs, weights)


def get_morphology_explanation(probs_before, probs_after, candidates):
    best_gain_i = 0
    best_gain = 0.0
    best_loss_i = 0
    best_loss = 0.0

    for i in range(len(candidates)):
        diff = probs_after[i] - probs_before[i]
        if diff > best_gain:
            best_gain = diff
            best_gain_i = i
        if diff < best_loss:
            best_loss = diff
            best_loss_i = i

    gainer = candidates[best_gain_i]
    loser = candidates[best_loss_i]

    note = gainer["morph_note"].split("—")[0].strip()
    text = f"Conditional update: morphological pattern makes '{gainer['gloss']}' more probable ({note}). "

    if abs(best_loss) > 0.02:
        loss_note = loser["morph_note"].split("—")[0].strip()
        text += f"'{loser['gloss']}' becomes less likely ({loss_note})."

    return text
