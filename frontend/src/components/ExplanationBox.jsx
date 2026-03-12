// Implementation: AI generated
const STAGE_CONFIG = {
  orthography: {
    icon: '📊',
    label: 'Empirical prior from corpus counts',
    concept: 'P(reading) estimated from corpus frequency via MLE with Laplace smoothing.',
  },
  morphology: {
    icon: '🔄',
    label: 'Conditional update: morphological evidence',
    concept: 'P(reading | morphology) ∝ P(reading) × P(pattern | reading)',
  },
  context: {
    icon: '🔄',
    label: 'Conditional update: sentence context',
    concept: 'P(reading | context) ∝ P(reading) × P(context | reading)',
  },
}

export default function ExplanationBox({ analysis, stage, probabilitySource, humanData }) {
  if (!analysis) return null

  if (probabilitySource === 'human') {
    const n = humanData?.responses ?? 0
    return (
      <div className="card explanation-card stage-border-orthography">
        <div className="explanation-stage-tag">
          <span className="explanation-icon">👤</span>
          <span className="explanation-stage-label">Human first guesses</span>
        </div>
        <p className="explanation-concept">
          P(reading) from first-guess counts: each proportion = count / total.
        </p>
        <p className="explanation-text">
          Based on {n} Arabic speakers' first guesses without context.
        </p>
      </div>
    )
  }

  const config = STAGE_CONFIG[stage] || STAGE_CONFIG.orthography

  return (
    <div className={`card explanation-card stage-border-${stage}`}>
      <div className="explanation-stage-tag">
        <span className="explanation-icon">{config.icon}</span>
        <span className="explanation-stage-label">{config.label}</span>
      </div>
      <p className="explanation-concept">{config.concept}</p>
      <p className="explanation-text">{analysis.explanation}</p>
    </div>
  )
}
