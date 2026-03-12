# Author: Faisal Almuhaysh
# Implementation: Developed with AI assistance

"""
sentence_scanner.py

CS109 Concept: Conditional probability estimation from observed evidence.

This module estimates P(sentence pattern | reading) — the likelihood
of observing a particular sentence structure if a given reading is
the correct one.

For example, if we observe the pattern [word] + [proper name] + [definite noun],
that pattern is much more likely under a verb reading than a noun reading,
because Arabic verb-subject-object sentences follow exactly this structure.

Each pattern rule in the data defines:
  - a condition to check (what tokens appear around the ambiguous word)
  - a likelihood weight per candidate reading

These likelihoods are then used in a Bayesian update:
  P(reading | sentence) ∝ P(reading) × P(sentence pattern | reading)

The rules are stored explicitly in examples.json, not hidden in code.
This module does NOT claim to understand arbitrary Arabic — it checks
a curated set of observable sentence patterns for the supported words.
"""

import re
from dataset_loader import get_examples


HARAKAT = set('\u064B\u064C\u064D\u064E\u064F\u0650\u0651\u0652\u0670')


def strip_diacritics(text):
    """Remove Arabic diacritical marks."""
    return ''.join(ch for ch in text if ch not in HARAKAT)


def strip_article(word):
    """Remove the definite article ال from the start of a word."""
    if word.startswith('ال') and len(word) > 2:
        return word[2:]
    return word


def normalize_for_matching(text):
    """Strip diacritics and normalize alef variants."""
    text = strip_diacritics(text)
    text = re.sub('[إأآا]', 'ا', text)
    text = text.replace('\u0640', '')
    return text


def build_surface_index():
    """Build lookup: normalized surface form → example entry."""
    examples = get_examples()
    index = {}
    for ex in examples:
        surface = normalize_for_matching(ex["surface"])
        index[surface] = ex
    return index


def tokenize_arabic(sentence):
    """Split Arabic sentence into tokens with character positions."""
    tokens = []
    pattern = re.compile(r'[\u0600-\u06FF\u0750-\u077F]+')
    for match in pattern.finditer(sentence):
        tokens.append({
            "text": match.group(),
            "start": match.start(),
            "end": match.end(),
        })
    return tokens


def scan_sentence(sentence):
    """
    Scan sentence for supported ambiguous words.
    Returns detected words with positions and example IDs.
    Also matches words with the definite article ال attached.
    """
    index = build_surface_index()
    tokens = tokenize_arabic(sentence)
    detected = []

    for token in tokens:
        normalized = normalize_for_matching(token["text"])
        bare = strip_article(normalized)

        match_key = None
        if normalized in index:
            match_key = normalized
        elif bare in index:
            match_key = bare

        if match_key:
            ex = index[match_key]
            detected.append({
                "surface_form": ex["surface"],
                "token_text": token["text"],
                "start": token["start"],
                "end": token["end"],
                "example_id": ex["id"],
            })

    return detected


# ══════════════════════════════════════════════════════════════
# Conditional probability estimation from sentence patterns
#
# Each function below checks for an observable feature in the
# sentence. These features let us estimate P(pattern | reading).
# ══════════════════════════════════════════════════════════════

# Common Arabic demonstratives
DEMONSTRATIVES = {"هذا", "هذه", "ذلك", "تلك", "هؤلاء", "أولئك"}

# Common Arabic prepositions and particles
PREPOSITIONS = {"في", "من", "إلى", "على", "عن", "مع", "بين", "حتى", "منذ", "عند"}

# Tokens that look like proper names: words without ال that aren't
# common particles. This is a heuristic — not a full NER system.
COMMON_PARTICLES = {
    "في", "من", "إلى", "على", "عن", "مع", "بين", "هو", "هي",
    "أن", "إن", "كان", "لم", "لن", "قد", "لا", "ما", "هل",
    "ثم", "أو", "و", "ف", "ب", "ل", "ك", "حتى", "منذ", "عند",
    "كل", "بعض", "غير", "هنا", "هناك", "أمس", "اليوم", "جداً",
    "كثيرة", "كثير", "جديدة", "جديد", "قديم", "قديمة",
    "كبير", "كبيرة", "صغير", "صغيرة", "طويل", "طويلة",
}

# Common adjective endings and patterns
ADJECTIVE_MARKERS = {"ة", "ية", "ي"}


def looks_like_proper_name(token_text):
    """
    Heuristic: a token that doesn't start with ال and isn't a common
    particle is likely a proper name or specific noun.
    """
    normalized = normalize_for_matching(token_text)
    if normalized in COMMON_PARTICLES:
        return False
    if normalized in DEMONSTRATIVES:
        return False
    if normalized in PREPOSITIONS:
        return False
    if normalized.startswith("ال"):
        return False
    if len(normalized) < 2:
        return False
    return True


def looks_like_definite_noun(token_text):
    """A token starting with ال is a definite noun."""
    normalized = normalize_for_matching(token_text)
    return normalized.startswith("ال") and len(normalized) > 2


def looks_like_adjective(token_text):
    """Heuristic: ends with typical adjective suffixes."""
    normalized = normalize_for_matching(token_text)
    for marker in ADJECTIVE_MARKERS:
        if normalized.endswith(marker) and len(normalized) > 3:
            return True
    return False


def compute_sentence_context_weights(sentence, candidates, example):
    """
    Estimate P(sentence pattern | reading) for each candidate.

    We observe the tokens around the ambiguous word and check them
    against curated pattern rules. Each rule that fires provides a
    likelihood estimate — how probable this sentence pattern would
    be if the word had a particular reading.

    When multiple rules fire, their likelihoods multiply (assuming
    conditional independence of the observed features, a standard
    simplifying assumption in CS109).

    Returns: (likelihood_dict, triggered_evidence_list)
    """
    sentence_norm = normalize_for_matching(sentence)
    surface_norm = normalize_for_matching(example["surface"])

    tokens = tokenize_arabic(sentence_norm)
    token_texts = [t["text"] for t in tokens]

    # Find the position of the ambiguous word in the token list
    # Also match when the article ال is attached (e.g., العلم matches علم)
    target_idx = -1
    for i, t in enumerate(token_texts):
        t_norm = normalize_for_matching(t)
        t_bare = strip_article(t_norm)
        if t_norm == surface_norm or t_bare == surface_norm:
            target_idx = i
            break

    if target_idx == -1:
        return {c["id"]: 1.0 for c in candidates}, []

    before = token_texts[:target_idx]
    after = token_texts[target_idx + 1:]

    triggered_cues = []
    cue_weights = {c["id"]: 1.0 for c in candidates}

    # Load pattern rules for this example
    pattern_rules = example.get("context_patterns", [])

    for rule in pattern_rules:
        rule_id = rule["id"]
        condition = rule["condition"]
        fired = False

        if condition == "followed_by_proper_name":
            if after and looks_like_proper_name(after[0]):
                fired = True

        elif condition == "followed_by_proper_then_definite":
            if len(after) >= 2 and looks_like_proper_name(after[0]) and looks_like_definite_noun(after[1]):
                fired = True

        elif condition == "preceded_by_demonstrative":
            if before and normalize_for_matching(before[-1]) in DEMONSTRATIVES:
                fired = True

        elif condition == "followed_by_adjective":
            if after and looks_like_adjective(after[0]):
                fired = True

        elif condition == "preceded_by_demonstrative_and_followed_by_adjective":
            has_demo = before and normalize_for_matching(before[-1]) in DEMONSTRATIVES
            has_adj = after and looks_like_adjective(after[0])
            if has_demo and has_adj:
                fired = True

        elif condition == "preceded_by_preposition":
            if before and normalize_for_matching(before[-1]) in PREPOSITIONS:
                fired = True

        elif condition == "sentence_initial_followed_by_noun":
            if target_idx == 0 and after and (looks_like_definite_noun(after[0]) or looks_like_proper_name(after[0])):
                fired = True

        elif condition == "followed_by_definite_noun":
            if after and looks_like_definite_noun(after[0]):
                fired = True

        elif condition == "preceded_by_definite_article_context":
            if before and looks_like_definite_noun(before[-1]):
                fired = True

        elif condition == "keyword_match":
            keywords = rule.get("keywords", [])
            sentence_tokens_bare = set()
            for t in token_texts:
                sentence_tokens_bare.add(normalize_for_matching(t))
                sentence_tokens_bare.add(strip_article(normalize_for_matching(t)))

            match_count = 0
            for kw in keywords:
                if normalize_for_matching(kw) in sentence_tokens_bare:
                    match_count += 1
            if match_count >= rule.get("min_matches", 1):
                fired = True

        if fired:
            triggered_cues.append({
                "rule_id": rule_id,
                "explanation": rule["explanation"],
            })
            for cand_id, weight in rule["weights"].items():
                cue_weights[cand_id] = cue_weights.get(cand_id, 1.0) * weight

    # Also check keyword matches from candidates as a fallback
    if not triggered_cues:
        sentence_tokens_bare = set()
        for t in token_texts:
            sentence_tokens_bare.add(normalize_for_matching(t))
            sentence_tokens_bare.add(strip_article(normalize_for_matching(t)))

        for candidate in candidates:
            keywords = candidate.get("context_keywords", [])
            match_count = 0
            for kw in keywords:
                if normalize_for_matching(kw) in sentence_tokens_bare:
                    match_count += 1

            if match_count >= 2:
                cue_weights[candidate["id"]] = cue_weights.get(candidate["id"], 1.0) * 2.0
                triggered_cues.append({
                    "rule_id": "keyword_fallback",
                    "explanation": f"Multiple context words suggest '{candidate['gloss']}'.",
                })
            elif match_count == 1:
                cue_weights[candidate["id"]] = cue_weights.get(candidate["id"], 1.0) * 1.4
                triggered_cues.append({
                    "rule_id": "keyword_fallback",
                    "explanation": f"A context word suggests '{candidate['gloss']}'.",
                })

    return cue_weights, triggered_cues


def get_sentence_context_explanation(triggered_cues, candidates, probs_after):
    """
    Generate a human-readable explanation of which evidence fired
    and how it changed the posterior distribution.
    """
    if not triggered_cues:
        return "The sentence context did not strongly favor one reading over others."

    top_idx = 0
    top_p = 0.0
    for i, p in enumerate(probs_after):
        if p > top_p:
            top_p = p
            top_idx = i

    top_cand = candidates[top_idx]
    pct = round(top_p * 100)

    primary_cue = triggered_cues[0]
    explanation = primary_cue["explanation"]

    return (
        f"'{top_cand['gloss']}' is now the dominant reading at {pct}%. "
        f"{explanation}"
    )
