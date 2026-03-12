// Implementation: AI generated
export default function EntropyMeter({
  entropyBits,
  entropyMax,
  entropyBase,
  topConfidence,
  numPlausible,
  evidenceLabel,
  stage,
}) {
  if (entropyBits == null || entropyMax == null) return null

  const pct = entropyMax > 0 ? (entropyBits / entropyMax) * 100 : 0
  const isLow = pct < 40
  const topPct = Math.round((topConfidence ?? 0) * 100)

  let delta = null
  if (entropyBase != null && stage !== 'orthography' && entropyBase > entropyBits) {
    delta = entropyBase - entropyBits
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
          {entropyBits.toFixed(2)} bits
          {delta != null && delta > 0.01 && (
            <span className="entropy-delta">(−{delta.toFixed(2)})</span>
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
        <span>{entropyMax.toFixed(2)} — max uncertainty</span>
      </div>

      <div className="entropy-stats">
        <div className="entropy-stat">
          <span className="entropy-stat-label" title="Readings with P ≥ 5%">
            Plausible readings
          </span>
          <span className="entropy-stat-value plausible">{numPlausible ?? 0}</span>
        </div>
        <div className="entropy-stat">
          <span className="entropy-stat-label" title="max(P(reading))">
            P(top reading)
          </span>
          <span className="entropy-stat-value confidence">{topPct}%</span>
        </div>
        <div className="entropy-stat">
          <span className="entropy-stat-label">Evidence</span>
          <span className="entropy-stat-value stage-tag">
            {evidenceLabel}
          </span>
        </div>
      </div>
    </div>
  )
}
