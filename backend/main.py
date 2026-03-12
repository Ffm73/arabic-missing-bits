# Author: Faisal Almuhaysh
# Implementation: Developed with AI assistance

"""
main.py — FastAPI backend for the Arabic Missing Bits demo.

Endpoints:
  GET  /examples          — list of available examples for the selector
  POST /analyze           — run probability analysis with toggles

In production, also serves the built React frontend as static files.
"""

import os
import sys

from fastapi import FastAPI, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional

from typing import List
from dataset_loader import find_example, find_context, get_example_summary, get_examples
from probability_engine import get_base_probabilities, normalize, top_confidence, num_plausible, bayesian_update
from morphology import apply_morphology, get_morphology_explanation
from context_model import apply_context, get_context_explanation
from sentence_scanner import scan_sentence, compute_sentence_context_weights, get_sentence_context_explanation
from entropy import entropy, max_entropy

app = FastAPI(title="The Missing Bits of Arabic")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BACKEND_DIR)
STATIC_DIR = os.path.join(PROJECT_ROOT, "frontend", "dist")

print(f"[startup] backend dir:  {BACKEND_DIR}", file=sys.stderr)
print(f"[startup] project root: {PROJECT_ROOT}", file=sys.stderr)
print(f"[startup] static dir:   {STATIC_DIR}", file=sys.stderr)
print(f"[startup] static exists: {os.path.isdir(STATIC_DIR)}", file=sys.stderr)


class AnalyzeRequest(BaseModel):
    example_id: str
    use_morphology: bool = False
    use_context: bool = False
    context_id: Optional[str] = None


@app.get("/examples")
def list_examples():
    """Return summaries of all available examples."""
    return get_example_summary()


@app.get("/examples/{example_id}")
def get_example_detail(example_id: str):
    """Return full detail for a single example."""
    ex = find_example(example_id)
    if ex is None:
        raise HTTPException(status_code=404, detail="Example not found")
    return ex


@app.post("/analyze")
def analyze(request: AnalyzeRequest):
    ex = find_example(request.example_id)
    if ex is None:
        raise HTTPException(status_code=404, detail="Example not found")

    candidates = ex["candidates"]

    # Stage 1: Base probabilities from corpus counts
    probs = get_base_probabilities(candidates)
    stage_name = "orthography"

    base_entropy = entropy(probs)
    base_probs = list(probs)

    stages = {
        "orthography": {
            "probs": [round(p, 4) for p in probs],
            "entropy": base_entropy,
        }
    }

    explanation = (
        f"From corpus counts alone, {ex['surface']} has "
        f"{num_plausible(probs)} plausible readings. "
        f"Entropy is {base_entropy:.2f} bits — the reader is uncertain."
    )

    # Stage 2: Morphology — conditional probability update
    if request.use_morphology:
        probs_before_morph = list(probs)
        probs = apply_morphology(probs, candidates)
        stage_name = "morphology"

        morph_entropy = entropy(probs)
        stages["morphology"] = {
            "probs": [round(p, 4) for p in probs],
            "entropy": morph_entropy,
            "delta": round(base_entropy - morph_entropy, 4),
        }

        explanation = get_morphology_explanation(
            probs_before_morph, probs, candidates
        )

    # Stage 3: Context — conditional probability update from sentence evidence
    if request.use_context:
        context = None
        if request.context_id:
            context = find_context(ex, request.context_id)
        elif ex.get("contexts"):
            context = ex["contexts"][0]

        if context is not None:
            probs_before_ctx = list(probs)
            probs = apply_context(probs, candidates, context)
            stage_name = "context"

            prev_entropy = entropy(probs_before_ctx)
            ctx_entropy = entropy(probs)
            stages["context"] = {
                "probs": [round(p, 4) for p in probs],
                "entropy": ctx_entropy,
                "delta": round(prev_entropy - ctx_entropy, 4),
                "context_used": {
                    "id": context["id"],
                    "sentence_ar": context["sentence_ar"],
                    "sentence_en": context["sentence_en"],
                }
            }

            explanation = get_context_explanation(
                probs_before_ctx, probs, candidates, context
            )

    # Build response
    current_entropy = entropy(probs)
    result_candidates = []
    for i in range(len(candidates)):
        c = candidates[i]
        result_candidates.append({
            "id": c["id"],
            "transliteration": c["transliteration"],
            "gloss": c["gloss"],
            "diacritized": c["diacritized"],
            "pos": c["pos"],
            "pos_detail": c.get("pos_detail", ""),
            "pattern": c.get("pattern", ""),
            "count": c["count"],
            "probability": round(probs[i], 4),
            "base_probability": round(base_probs[i], 4),
            "morph_note": c.get("morph_note", ""),
        })

    return {
        "example_id": ex["id"],
        "surface_form": ex["surface"],
        "root": ex["root"],
        "root_translit": ex["root_translit"],
        "root_meaning": ex["root_meaning"],
        "ambiguity_note": ex["ambiguity_note"],
        "stage": stage_name,
        "candidates": result_candidates,
        "entropy_bits": current_entropy,
        "entropy_max": max_entropy(len(candidates)),
        "entropy_base": base_entropy,
        "num_plausible": num_plausible(probs),
        "top_confidence": round(top_confidence(probs), 4),
        "explanation": explanation,
        "stages": stages,
    }


# ── Sentence scanning for "Try a Sentence" mode ──

class ScanRequest(BaseModel):
    sentence: str


class AnalyzeSentenceRequest(BaseModel):
    sentence: str
    example_id: str
    use_morphology: bool = False
    use_context: bool = False


@app.post("/scan_sentence")
def scan(request: ScanRequest):
    """
    Scan a sentence for supported ambiguous words.
    Returns detected words with positions for highlighting.
    """
    detected = scan_sentence(request.sentence)

    suggested = []
    if not detected:
        examples = get_examples()
        for ex in examples[:5]:
            sents = ex.get("suggested_sentences", [])
            if sents:
                suggested.append(sents[0])

    return {
        "sentence": request.sentence,
        "detected_words": detected,
        "suggested_sentences": suggested,
    }


@app.post("/analyze_sentence")
def analyze_from_sentence(request: AnalyzeSentenceRequest):
    """
    Analyze a word found in a user-typed sentence.
    Uses the sentence itself as context evidence via keyword matching.
    """
    ex = find_example(request.example_id)
    if ex is None:
        raise HTTPException(status_code=404, detail="Example not found")

    candidates = ex["candidates"]

    probs = get_base_probabilities(candidates)
    stage_name = "orthography"
    base_entropy = entropy(probs)
    base_probs = list(probs)

    stages = {
        "orthography": {
            "probs": [round(p, 4) for p in probs],
            "entropy": base_entropy,
        }
    }

    explanation = (
        f"From corpus counts alone, {ex['surface']} has "
        f"{num_plausible(probs)} plausible readings. "
        f"Entropy is {base_entropy:.2f} bits — the reader is uncertain."
    )

    if request.use_morphology:
        probs_before = list(probs)
        probs = apply_morphology(probs, candidates)
        stage_name = "morphology"
        morph_entropy = entropy(probs)
        stages["morphology"] = {
            "probs": [round(p, 4) for p in probs],
            "entropy": morph_entropy,
            "delta": round(base_entropy - morph_entropy, 4),
        }
        explanation = get_morphology_explanation(probs_before, probs, candidates)

    if request.use_context:
        cue_weights, triggered_cues = compute_sentence_context_weights(
            request.sentence, candidates, ex
        )

        weight_list = []
        for c in candidates:
            weight_list.append(cue_weights.get(c["id"], 1.0))

        has_signal = any(w != 1.0 for w in weight_list)

        if has_signal:
            probs_before = list(probs)
            probs = bayesian_update(probs, weight_list)
            stage_name = "context"

            prev_entropy = entropy(probs_before)
            ctx_entropy = entropy(probs)

            ctx_explanation = get_sentence_context_explanation(
                triggered_cues, candidates, probs
            )

            stages["context"] = {
                "probs": [round(p, 4) for p in probs],
                "entropy": ctx_entropy,
                "delta": round(prev_entropy - ctx_entropy, 4),
                "context_used": {
                    "id": "sentence",
                    "sentence_ar": request.sentence,
                    "sentence_en": "(user-provided sentence)",
                }
            }
            explanation = ctx_explanation
        else:
            explanation += " The surrounding words did not strongly favor one reading."

    current_entropy = entropy(probs)
    result_candidates = []
    for i in range(len(candidates)):
        c = candidates[i]
        result_candidates.append({
            "id": c["id"],
            "transliteration": c["transliteration"],
            "gloss": c["gloss"],
            "diacritized": c["diacritized"],
            "pos": c["pos"],
            "pos_detail": c.get("pos_detail", ""),
            "pattern": c.get("pattern", ""),
            "count": c["count"],
            "probability": round(probs[i], 4),
            "base_probability": round(base_probs[i], 4),
            "morph_note": c.get("morph_note", ""),
        })

    return {
        "example_id": ex["id"],
        "surface_form": ex["surface"],
        "root": ex["root"],
        "root_translit": ex["root_translit"],
        "root_meaning": ex["root_meaning"],
        "ambiguity_note": ex["ambiguity_note"],
        "stage": stage_name,
        "candidates": result_candidates,
        "entropy_bits": current_entropy,
        "entropy_max": max_entropy(len(candidates)),
        "entropy_base": base_entropy,
        "num_plausible": num_plausible(probs),
        "top_confidence": round(top_confidence(probs), 4),
        "explanation": explanation,
        "stages": stages,
    }


# ── Health check for Render ──

@app.get("/health")
def health():
    return {"status": "ok"}


# ── Serve built React frontend in production ──

assets_dir = os.path.join(STATIC_DIR, "assets")
index_html = os.path.join(STATIC_DIR, "index.html")

if os.path.isdir(STATIC_DIR) and os.path.isdir(assets_dir):
    print(f"[startup] Mounting static frontend from {STATIC_DIR}", file=sys.stderr)
    app.mount("/assets", StaticFiles(directory=assets_dir), name="static-assets")

    @app.get("/")
    async def serve_index():
        return FileResponse(index_html)

    @app.get("/{full_path:path}")
    async def serve_spa(request: Request, full_path: str):
        file_path = os.path.join(STATIC_DIR, full_path)
        if full_path and os.path.isfile(file_path):
            return FileResponse(file_path)
        return FileResponse(index_html)
else:
    print(f"[startup] No static frontend found at {STATIC_DIR}", file=sys.stderr)
