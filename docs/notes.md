<!-- Author: Faisal Almuhaysh. Implementation: Developed with AI assistance -->
# Development Notes

## Data Sources

The 10 curated examples in `data/examples.json` were selected for:
- Genuine ambiguity (at least 2 plausible readings with non-trivial probability)
- Clear, understandable glosses for non-Arabic speakers
- Interesting root semantics (e.g., "heart" and "to flip" sharing the root q-l-b)
- Coverage of different part-of-speech contrasts (noun vs. verb, active vs. passive)

### Corpus frequency estimates

Counts are estimated from frequency patterns consistent with the Tashkeela
diacritized corpus (~75 million words). The exact values are approximate
but preserve realistic relative magnitudes:
- High-frequency nouns: 1500–3200 occurrences
- Common verbs: 500–1600 occurrences
- Passive forms: typically 5–15% of active form counts

### Morphology weights

Based on documented Arabic morphological productivity:
- The fa'ala pattern (active past verb, Form I) is the most productive verb form
- The fu'ila pattern (passive past verb) accounts for ~3% of verb tokens
- Common noun patterns (fa'l, fi'l, fu'l) are among the most frequent in Arabic

Source: Arabic morphological studies and corpus linguistics literature.

### Context weights

Hand-curated for demonstration. Each context scenario uses a real Arabic sentence
where the surrounding words clearly favor one reading. The weight values (typically
0.2–2.8) are designed to produce visible and realistic probability shifts.

## Design Decisions

1. **Laplace smoothing (α=0.5):** Prevents zero probabilities for rare forms.
   Standard choice for small count data.

2. **Bayesian multiplication for updates:** P_new ∝ P_old × weight, then normalize.
   This is the simplest principled update and matches CS109 teaching.

3. **Pre-computed morphology weights:** Rather than running a morphological analyzer
   at runtime, weights are stored in the data. This keeps the demo fast and the
   logic transparent.

4. **Two context sentences per word:** Enough to show that different contexts
   favor different readings, without overwhelming the UI.

## What This Demo Does NOT Claim

- It is not a general-purpose Arabic diacritizer
- The context model is not trained on co-occurrence data
- The morphology layer does not perform full morphological analysis
- The probabilities are estimates, not exact corpus measurements

The goal is to demonstrate the *concept* of ambiguity resolution through
probability, not to build a production system.
