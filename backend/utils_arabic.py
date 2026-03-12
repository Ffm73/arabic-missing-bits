# Author: Faisal Almuhaysh
# Implementation: Developed with AI assistance

"""
utils_arabic.py

Utility functions for Arabic text processing.
These handle diacritic stripping and normalization — the core operations
needed to understand why Arabic text can be ambiguous.
"""

import re

# Arabic diacritical marks (harakat) — these are the "missing bits"
HARAKAT = {
    '\u064B',  # fatḥatan  ً   (accusative indefinite)
    '\u064C',  # ḍammatan  ٌ   (nominative indefinite)
    '\u064D',  # kasratan  ٍ   (genitive indefinite)
    '\u064E',  # fatḥa     َ   (a vowel)
    '\u064F',  # ḍamma     ُ   (u vowel)
    '\u0650',  # kasra     ِ   (i vowel)
    '\u0651',  # shadda    ّ   (consonant doubling)
    '\u0652',  # sukūn     ْ   (no vowel)
    '\u0670',  # dagger alif ٰ (superscript alif)
}


def strip_diacritics(text):
    """
    Remove all Arabic diacritical marks from a string.
    This simulates how everyday Arabic is actually written.
    """
    result = []
    for char in text:
        if char not in HARAKAT:
            result.append(char)
    return ''.join(result)


def has_diacritics(text):
    """Check whether text contains any Arabic diacritical marks."""
    for char in text:
        if char in HARAKAT:
            return True
    return False


def normalize_arabic(text):
    """
    Light normalization for Arabic text:
    - Strip diacritics
    - Normalize alef variants to plain alef
    - Remove tatweel (kashida)
    """
    text = strip_diacritics(text)
    text = re.sub('[إأآا]', 'ا', text)
    text = text.replace('\u0640', '')
    return text
