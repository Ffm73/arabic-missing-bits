<!-- Author: Faisal Almuhaysh. Implementation: Developed with AI assistance -->
# The Missing Bits of Arabic

**CS109 — Probability for Computer Scientists — Final Challenge Project**

An interactive demo showing how Arabic readers resolve ambiguity in vowel-less text, and how that process can be measured using entropy from information theory.

## The Idea

Arabic is usually written without short vowels. These omitted marks — called **harakat** (حَرَكَات) — are the "missing bits." Without them, a single written form can correspond to several completely different words.

For example, the letters **كتب** could be read as:

| Reading | Transliteration | Meaning |
|---------|----------------|---------|
| كُتُب | kutub | books |
| كَتَبَ | kataba | he wrote |
| كُتِبَ | kutiba | it was written |

Native readers resolve this ambiguity effortlessly using two sources of evidence:
1. **Morphology** — Arabic words are built from roots and patterns. Some patterns (like the active verb form fa'ala) are far more common than others (like the passive fu'ila).
2. **Context** — Surrounding words narrow down the possibilities. "In the library..." almost certainly means "books," not "he wrote."

This demo makes that process visible and measurable.

## Quick Start

### 1. Install Python dependencies

```bash
cd arabic-missing-bits
pip install -r requirements.txt
```

### 2. Generate the dataset (optional — already included)

```bash
python scripts/build_examples.py
```

### 3. Start the backend

```bash
cd backend
uvicorn main:app --reload --port 8000
```

### 4. Start the frontend

```bash
cd frontend
npm install
npm run dev
```

Then open **http://localhost:5173** in your browser.

## How It Works

### Stage 1: Orthography Only

With just the bare consonantal form, all readings are possible. The system assigns base probabilities estimated from how often each diacritized form appears in corpus data. Entropy is relatively high.

### Stage 2: Morphology

Toggle on **Morphology** to apply structural evidence. Arabic morphology is built on a root-and-pattern system — a 3-consonant root (like k-t-b) is interleaved with vowel patterns (like fu'ul, fa'ala) to create different word forms. Some patterns are far more productive than others:

- Active verb forms (fa'ala) are very common → probability increases
- Passive verb forms (fu'ila) are rare (~3% of verb tokens) → probability decreases
- Common noun patterns (fa'l, fu'ul) are frequent → probability adjusts accordingly

Entropy decreases as implausible readings are down-weighted.

### Stage 3: Context

Toggle on **Context** to apply sentence-level evidence. Select from curated context sentences to see how surrounding words collapse the distribution. For example:

- *"In the library there are many ___"* → "books" jumps to ~91%
- *"The student ___ a letter to his friend"* → "he wrote" dominates

Entropy drops further, often dramatically.

## Key Terms

- **Harakat (حَرَكَات):** Short vowel marks in Arabic writing — the small marks above and below letters that indicate pronunciation. Usually omitted in everyday text.
- **Morphology:** How words are built from roots and patterns. In Arabic, the root k-t-b (writing) combines with different vowel patterns to produce "books," "he wrote," "writer," etc.
- **Entropy:** A measure of uncertainty from information theory. More ambiguity = more bits. When one reading dominates, entropy is low.
- **Candidate reading:** One possible pronunciation and meaning for an undiacritized written form.

## Data Grounding

The base probabilities come from frequency patterns consistent with the [Tashkeela](https://sourceforge.net/projects/tashkeela/) diacritized Arabic corpus. For each undiacritized form, we count how often each diacritized variant appears, then apply Laplace smoothing.

Morphology weights reflect documented Arabic morphological productivity — how common each word-building pattern is in actual usage.

Context weights are hand-curated for the demo's example set. In a full system, these would come from co-occurrence statistics in a large corpus. The curated values are designed to be realistic and illustrative. All context scenarios use real Arabic sentences.

The **human first-guess** layer is based on a small number of Arabic speakers' first responses (e.g. 8 per word in the included data). To estimate how stable those proportions are, the project uses **bootstrap resampling**: it repeatedly resamples the responses with replacement and recomputes the probability of each reading. The result is a 90% percentile interval for each reading (e.g. [0.40, 0.72]), shown on hover in the Human vs Model view.

### What is intentionally simple

This demo is a proof-of-concept, not a production NLP system. Several design choices keep it understandable:

- The example set is small (10 words) and manually curated for demo quality
- Morphology weights are precomputed, not dynamically analyzed
- Context is selected from pre-defined sentences, not extracted from free text
- All probability updates use simple Bayesian multiplication and renormalization

These simplifications are deliberate — they keep the math transparent and the demo focused on the core insight.

## Project Structure

```
arabic-missing-bits/
├── backend/
│   ├── main.py                  # FastAPI endpoints
│   ├── probability_engine.py    # normalize, smooth, update (CS109-style)
│   ├── bootstrap_human.py       # bootstrap resampling for human first-guess uncertainty
│   ├── entropy.py               # H = -Σ p log₂ p
│   ├── morphology.py            # morphological evidence updates
│   ├── context_model.py         # contextual evidence updates
│   ├── dataset_loader.py        # loads examples.json
│   └── utils_arabic.py          # diacritic stripping, normalization
├── data/
│   └── examples.json            # curated ambiguous word dataset
├── scripts/
│   ├── build_examples.py        # generates examples.json from curated data
│   └── preprocess_corpus.py     # template for real corpus processing
├── frontend/
│   ├── src/
│   │   ├── App.jsx              # main app with state management
│   │   ├── components/
│   │   │   ├── WordDisplay.jsx
│   │   │   ├── CandidateList.jsx
│   │   │   ├── EntropyMeter.jsx
│   │   │   ├── TogglePanel.jsx
│   │   │   └── ExplanationBox.jsx
│   │   └── styles/app.css
│   └── index.html
├── requirements.txt
└── README.md
```

## API

### `GET /examples`
Returns summaries of all available example words.

### `GET /examples/{id}`
Returns full detail for a single example.

### `POST /analyze`
Run probability analysis with optional morphology and context.

```json
{
  "example_id": "ktb",
  "use_morphology": true,
  "use_context": true,
  "context_id": "library"
}
```

Returns candidates with probabilities, entropy, plausible reading count, top confidence, stage breakdowns, and a natural-language explanation.

## The English Analogy

Before diving into Arabic, consider this English sentence:

> *"I saw her duck."*

Does "duck" mean the animal, or does it mean she ducked down? You resolve this instantly from context — but a computer sees genuine ambiguity. Arabic faces this same challenge on a much larger scale, because the vowels that distinguish words are systematically omitted from everyday writing.
