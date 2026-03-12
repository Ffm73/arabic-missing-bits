<!-- Author: Faisal Almuhaysh. Implementation: Developed with AI assistance -->
# File classification report

## Classification table

| File | Purpose | Technologies | Classification |
|------|---------|--------------|----------------|
| backend/probability_engine.py | Normalization, MLE, Laplace smoothing, Bayesian update | Python | WRITTEN BY ME |
| backend/entropy.py | Shannon entropy H = −Σ p log₂ p, max entropy | Python | WRITTEN BY ME |
| backend/morphology.py | Morphology likelihood weights, Bayesian update | Python | WRITTEN BY ME |
| backend/context_model.py | Context likelihood weights, Bayesian update | Python | WRITTEN BY ME |
| backend/bootstrap_human.py | Bootstrap resampling for human first-guess uncertainty | Python | WRITTEN BY ME |
| backend/sentence_scanner.py | Sentence pattern detection, P(pattern \| reading) for context | Python | WRITTEN BY ME |
| backend/main.py | FastAPI app, endpoints, pipeline orchestration | Python | WRITTEN WITH AI ASSISTANCE |
| backend/dataset_loader.py | Load examples.json, find example/context | Python | WRITTEN WITH AI ASSISTANCE |
| backend/utils_arabic.py | Strip diacritics, normalize Arabic text | Python | WRITTEN WITH AI ASSISTANCE |
| scripts/build_examples.py | Generate examples.json from curated data | Python | WRITTEN WITH AI ASSISTANCE |
| scripts/preprocess_corpus.py | Template for corpus preprocessing | Python | WRITTEN WITH AI ASSISTANCE |
| scripts/add_context_keywords.py | Patch examples.json with context keywords | Python | WRITTEN BY AI |
| scripts/add_context_patterns.py | Patch examples.json with context patterns | Python | WRITTEN BY AI |
| frontend/src/App.jsx | Main app state, probability source, active distribution | React, JSX | WRITTEN BY AI |
| frontend/src/main.jsx | Entry point | React, JSX | WRITTEN BY AI |
| frontend/src/components/CandidateList.jsx | Candidate bars and human/model display | React, JSX | WRITTEN BY AI |
| frontend/src/components/EntropyMeter.jsx | Entropy and stats display | React, JSX | WRITTEN BY AI |
| frontend/src/components/EvidenceWaterfall.jsx | Probability trace by stage | React, JSX | WRITTEN BY AI |
| frontend/src/components/ExplanationBox.jsx | Stage and human explanation text | React, JSX | WRITTEN BY AI |
| frontend/src/components/ModeSwitch.jsx | Curated / Try a Sentence mode | React, JSX | WRITTEN BY AI |
| frontend/src/components/ProbabilitySourceSwitch.jsx | Human Intuition / Model Reasoning | React, JSX | WRITTEN BY AI |
| frontend/src/components/SentenceInput.jsx | Sentence input and word selection | React, JSX | WRITTEN BY AI |
| frontend/src/components/TogglePanel.jsx | Morphology and context toggles | React, JSX | WRITTEN BY AI |
| frontend/src/components/WordDisplay.jsx | Word display and navigation | React, JSX | WRITTEN BY AI |
| frontend/src/styles/app.css | Application styles | CSS | WRITTEN BY AI |
| frontend/src/App.css | Unused placeholder | CSS | WRITTEN BY AI |
| frontend/src/index.css | Unused placeholder | CSS | WRITTEN BY AI |
| frontend/index.html | HTML shell | HTML | WRITTEN BY AI |
| frontend/vite.config.js | Vite build config | JavaScript | WRITTEN BY AI |
| frontend/eslint.config.js | ESLint config | JavaScript | WRITTEN BY AI |
| run.py | Production startup script | Python | WRITTEN BY AI |
| README.md | Project documentation | Markdown | WRITTEN WITH AI ASSISTANCE |
| docs/notes.md | Development notes | Markdown | WRITTEN WITH AI ASSISTANCE |
| docs/CLASSIFICATION.md | This classification report | Markdown | WRITTEN WITH AI ASSISTANCE |
| requirements.txt | Python dependencies | Text | Config |
| render.yaml | Render deployment config | YAML | Config |
| data/examples.json | Curated ambiguous-word dataset | JSON | Data |
| data/human_intuition.json | Human first-guess counts | JSON | Data |
| data/counterfactual_pairs.json | Counterfactual sentence pairs | JSON | Data |

## Summary by category

- **Probability modeling (WRITTEN BY ME):** probability_engine.py, entropy.py, morphology.py, context_model.py, bootstrap_human.py, sentence_scanner.py. All CS109-related probability logic (distributions, MLE, smoothing, normalization, entropy, Bayesian updates, conditional probability, bootstrap) is implemented in these files and appears as author-written student code.

- **Data processing:** dataset_loader.py, utils_arabic.py (WRITTEN WITH AI ASSISTANCE); build_examples.py, preprocess_corpus.py (WRITTEN WITH AI ASSISTANCE); add_context_keywords.py, add_context_patterns.py (WRITTEN BY AI). Data files (examples.json, human_intuition.json, etc.) are curated or generated data.

- **Backend API:** main.py (WRITTEN WITH AI ASSISTANCE) orchestrates the pipeline and exposes FastAPI endpoints; it calls the probability modules above.

- **Frontend interface:** All React components, styles, and frontend config (WRITTEN BY AI) implement the UI; they consume API data and do not contain probability logic.

## File header format

- **WRITTEN BY ME:** `# Author: Faisal Almuhaysh` and `# Implementation: Written by author`
- **WRITTEN WITH AI ASSISTANCE:** `# Author: Faisal Almuhaysh` and `# Implementation: Developed with AI assistance`
- **WRITTEN BY AI:** `# Implementation: AI generated` (or `//` / `/* */` as appropriate for the language)
