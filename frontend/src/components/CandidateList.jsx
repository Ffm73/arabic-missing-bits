// Implementation: AI generated
const BAR_COLORS = ['var(--bar-1)', 'var(--bar-2)', 'var(--bar-3)', 'var(--bar-4)']

export default function CandidateList({ analysis }) {
  if (!analysis) return null

  const candidates = [...analysis.candidates].sort((a, b) => b.probability - a.probability)

  return (
    <div className="card candidates-card">
      <div className="candidates-header">
        <span>Candidate reading</span>
        <span>P(reading)</span>
      </div>
      {candidates.map((c, i) => {
        const pct = Math.round(c.probability * 100)
        const color = BAR_COLORS[Math.min(i, BAR_COLORS.length - 1)]
        const rankClass = `rank-${Math.min(i + 1, 4)}`

        return (
          <div className="candidate-row" key={c.id}>
            <div className={`candidate-rank ${rankClass}`}>{i + 1}</div>
            <div className="candidate-info">
              <div className="candidate-main-line">
                <span className="candidate-translit">{c.transliteration}</span>
                <span className="candidate-diacritized">{c.diacritized}</span>
                <span className="candidate-pos">{c.pos.replace('_', ' ')}</span>
              </div>
              <div className="candidate-gloss">
                {c.gloss}
                <span className="candidate-count" title="Corpus frequency count">
                  {' '}· {c.count.toLocaleString()} occurrences
                </span>
              </div>
            </div>
            <div className="candidate-bar-area">
              <div className="candidate-bar-track">
                <div
                  className="candidate-bar-fill"
                  style={{ width: `${pct}%`, background: color }}
                />
              </div>
              <span className="candidate-pct">{pct}%</span>
            </div>
          </div>
        )
      })}
    </div>
  )
}
