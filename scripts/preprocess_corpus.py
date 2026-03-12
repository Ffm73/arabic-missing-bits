# Author: Faisal Almuhaysh
# Implementation: Developed with AI assistance

"""
preprocess_corpus.py

Template script for processing a real diacritized Arabic corpus (e.g., Tashkeela)
into a frequency table of ambiguous undiacritized forms.

To use this script with real data:
  1. Download a diacritized corpus (e.g., https://sourceforge.net/projects/tashkeela/)
  2. Place text files in data/raw/
  3. Run: python scripts/preprocess_corpus.py

The output is data/processed/ambiguous_forms.json — a lookup table mapping each
undiacritized surface form to its diacritized variants and their counts.
"""

import json
import os
import re
from collections import defaultdict

# ── Arabic diacritic marks (Unicode) ────────────────────────────────

HARAKAT = {
    '\u064B',  # fatḥatan (ً)
    '\u064C',  # ḍammatan (ٌ)
    '\u064D',  # kasratan (ٍ)
    '\u064E',  # fatḥa (َ)
    '\u064F',  # ḍamma (ُ)
    '\u0650',  # kasra (ِ)
    '\u0651',  # shadda (ّ)
    '\u0652',  # sukūn (ْ)
    '\u0670',  # superscript alif (ٰ)
}


def strip_diacritics(text):
    """Remove all Arabic diacritical marks from text."""
    result = []
    for char in text:
        if char not in HARAKAT:
            result.append(char)
    return ''.join(result)


def normalize_arabic(text):
    """
    Light normalization:
    - Remove diacritics
    - Normalize alef variants to plain alef
    - Normalize tā' marbūṭa
    - Remove tatweel
    """
    text = strip_diacritics(text)

    # Normalize alef variants
    text = re.sub('[إأآا]', 'ا', text)

    # Remove tatweel (kashida)
    text = text.replace('\u0640', '')

    return text


def has_diacritics(word):
    """Check if a word contains any diacritical marks."""
    for char in word:
        if char in HARAKAT:
            return True
    return False


def extract_words(text):
    """Extract individual Arabic words from text."""
    arabic_pattern = re.compile(r'[\u0600-\u06FF]+')
    return arabic_pattern.findall(text)


def process_corpus(raw_dir, output_path, min_ambiguity=2, min_total_count=10):
    """
    Process all text files in raw_dir:
    1. Extract diacritized words
    2. Strip diacritics to get surface forms
    3. Group diacritized variants by surface form
    4. Keep only genuinely ambiguous cases
    5. Export counts
    """
    # Count: surface_form -> {diacritized_form -> count}
    form_counts = defaultdict(lambda: defaultdict(int))

    if not os.path.exists(raw_dir):
        print(f"No raw data directory found at {raw_dir}")
        print("To use this script:")
        print("  1. Download a diacritized corpus (e.g., Tashkeela)")
        print("  2. Place .txt files in data/raw/")
        print("  3. Re-run this script")
        return

    txt_files = [f for f in os.listdir(raw_dir) if f.endswith('.txt')]

    if not txt_files:
        print(f"No .txt files found in {raw_dir}")
        return

    total_words = 0
    total_diacritized = 0

    for filename in txt_files:
        filepath = os.path.join(raw_dir, filename)
        print(f"Processing {filename}...")

        with open(filepath, 'r', encoding='utf-8') as f:
            text = f.read()

        words = extract_words(text)
        total_words += len(words)

        for word in words:
            if has_diacritics(word) and len(strip_diacritics(word)) >= 2:
                surface = normalize_arabic(word)
                form_counts[surface][word] += 1
                total_diacritized += 1

    print(f"\nProcessed {total_words} total words, {total_diacritized} diacritized")

    # Filter to genuinely ambiguous forms
    ambiguous = {}
    for surface, variants in form_counts.items():
        if len(variants) < min_ambiguity:
            continue

        total = sum(variants.values())
        if total < min_total_count:
            continue

        ambiguous[surface] = {
            "surface": surface,
            "total_count": total,
            "num_variants": len(variants),
            "variants": [
                {"diacritized": form, "count": count}
                for form, count in sorted(variants.items(), key=lambda x: -x[1])
            ]
        }

    print(f"Found {len(ambiguous)} ambiguous forms (>= {min_ambiguity} variants, >= {min_total_count} total)")

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(ambiguous, f, ensure_ascii=False, indent=2)

    print(f"Saved to {output_path}")

    # Show top examples
    top = sorted(ambiguous.values(), key=lambda x: -x["total_count"])[:20]
    print("\nTop 20 ambiguous forms by frequency:")
    for entry in top:
        variants_str = ", ".join(
            f"{v['diacritized']}({v['count']})"
            for v in entry["variants"][:4]
        )
        print(f"  {entry['surface']}: {entry['total_count']} total, "
              f"{entry['num_variants']} variants — {variants_str}")


if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    project_dir = os.path.join(script_dir, "..")

    raw_dir = os.path.join(project_dir, "data", "raw")
    output_path = os.path.join(project_dir, "data", "processed", "ambiguous_forms.json")

    process_corpus(raw_dir, output_path)
