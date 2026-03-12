# Author: Faisal Almuhaysh
# Implementation: Developed with AI assistance

"""
dataset_loader.py

Loads the curated examples from data/examples.json.
"""

import json
import os

DATA_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "examples.json")

_cache = None
_cache_mtime = 0


def load_dataset():
    """Load the dataset, re-reading from disk if the file has changed."""
    global _cache, _cache_mtime

    mtime = os.path.getmtime(DATA_PATH)

    if _cache is not None and mtime == _cache_mtime:
        return _cache

    with open(DATA_PATH, "r", encoding="utf-8") as f:
        data = json.load(f)

    _cache = data
    _cache_mtime = mtime
    return data


def get_examples():
    """Return list of all example entries."""
    data = load_dataset()
    return data["examples"]


def find_example(example_id):
    """
    Look up a specific example by its ID.
    Returns the example dict or None.
    """
    examples = get_examples()

    for ex in examples:
        if ex["id"] == example_id:
            return ex

    return None


def find_context(example, context_id):
    """
    Look up a specific context scenario within an example.
    Returns the context dict or None.
    """
    if example is None:
        return None

    for ctx in example.get("contexts", []):
        if ctx["id"] == context_id:
            return ctx

    return None


def get_example_summary():
    """
    Return a lightweight summary of all examples for the frontend selector.
    """
    examples = get_examples()
    summaries = []

    for ex in examples:
        summaries.append({
            "id": ex["id"],
            "surface": ex["surface"],
            "root_translit": ex["root_translit"],
            "root_meaning": ex["root_meaning"],
            "num_candidates": len(ex["candidates"]),
            "contexts": [
                {"id": ctx["id"], "sentence_en": ctx["sentence_en"]}
                for ctx in ex.get("contexts", [])
            ]
        })

    return summaries
