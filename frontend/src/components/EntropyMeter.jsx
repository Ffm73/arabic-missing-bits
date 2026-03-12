// Implementation: AI generated
export default function EntropyMeter({ analysis, stage }) {
  if (!analysis) return null

  const { entropy_bits, entropy_max, entropy_base, num_plausible, top_confidence, stages } = analysis

  const pct = entropy_max > 0 ? (entropy_bits / entropy_max) * 100 : 0
  const isLow = pct < 40
  const topPct = Math.round(top_confidence * 100)

  let delta = null
  if (stage !== 'orthography') {
    delta = entropy_base - entropy_bits
  }

  const CS109_LABELS = {
    orthography: 'Prior only',
    morphology: 'Prior × morphology',
    context: 'Prior × morph × context',
  }

  return (
    <div className="card entropy-card">
      <div className="entropy-top-row">
        <span
          className="entropy-label"
          title="H(X) = −Σ p(x) log₂ p(x). Measures remaining uncertainty in bits."
        >
          Entropy (uncertainty)
        </span>
        <span className="entropy-bits">
          {entropy_bits.toFixed(2)} bits
          {delta !== null && delta > 0.01 && (
            <span className="entropy-delta">
              (−{delta.toFixed(2)})
            </span>
          )}
        </span>
      </div>

      <div className="entropy-bar-track">
        <div
          className={`entropy-bar-fill ${isLow ? 'low' : ''}`}
          style={{ width: `${pct}%` }}
        />
      </div>

      <div className="entropy-scale">
        <span>0 — certain</span>
        <span>{entropy_max.toFixed(2)} — max uncertainty</span>
      </div>

      <div className="entropy-stats">
        <div className="entropy-stat">
          <span className="entropy-stat-label" title="Readings with P ≥ 5%">
            Plausible readings
          </span>
          <span className="entropy-stat-value plausible">{num_plausible}</span>
        </div>
        <div className="entropy-stat">
          <span className="entropy-stat-label" title="max(P(reading))">
            P(top reading)
          </span>
          <span className="entropy-stat-value confidence">{topPct}%</span>
        </div>
        <div className="entropy-stat">
          <span className="entropy-stat-label">Evidence</span>
          <span className={`entropy-stat-value stage-tag stage-${stage}`}>
            {CS109_LABELS[stage] || stage}
          </span>
        </div>
      </div>
    </div>
  )
}
