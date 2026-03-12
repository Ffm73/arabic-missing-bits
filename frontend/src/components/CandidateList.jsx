// Implementation: AI generated
const BAR_COLORS = ['var(--bar-1)', 'var(--bar-2)', 'var(--bar-3)', 'var(--bar-4)']

export default function CandidateList({ activeDistribution, probabilitySource, humanData }) {
  const isHuman = probabilitySource === 'human'

  if (!activeDistribution?.length) return null

  return (
    <div className="card candidates-card">
      <div className="candidates-header">
        <span>Candidate reading</span>
        <span>P(reading)</span>
      </div>
      {activeDistribution.map((c, i) => {
        const displayPct = Math.round(c.probability * 100)
        const color = BAR_COLORS[Math.min(i, BAR_COLORS.length - 1)]
        const rankClass = `rank-${Math.min(i + 1, 4)}`
        const boot = isHuman && humanData?.bootstrap?.[c.id]
        const bootstrapTitle = boot
          ? `Observed: ${(humanData.human_probs[c.id] ?? 0).toFixed(2)} · Bootstrap 90%: [${boot.low.toFixed(2)}, ${boot.high.toFixed(2)}]`
          : undefined

        return (
          <div className="candidate-row" key={c.id} title={bootstrapTitle}>
            <div className={`candidate-rank ${rankClass}`}>{i + 1}</div>
            <div className="candidate-info">
              <div className="candidate-main-line">
                <span className="candidate-translit">{c.transliteration}</span>
                <span className="candidate-diacritized">{c.diacritized}</span>
                <span className="candidate-pos">{c.pos.replace('_', ' ')}</span>
              </div>
              <div className="candidate-gloss">
                {c.gloss}
                {!isHuman && (
                  <span className="candidate-count" title="Corpus frequency count">
                    {' '}· {c.count.toLocaleString()} occurrences
                  </span>
                )}
                {isHuman && humanData && (
                  <span className="candidate-count">
                    {' '}· {humanData.guesses[c.id] ?? 0}/{humanData.responses} speakers chose this
                  </span>
                )}
              </div>
            </div>
            <div className="candidate-bar-area">
              <div className="candidate-bar-track">
                <div
                  className="candidate-bar-fill"
                  style={{
                    width: `${displayPct}%`,
                    background: isHuman ? 'var(--green)' : color,
                  }}
                />
              </div>
              <span className="candidate-pct">{displayPct}%</span>
            </div>
          </div>
        )
      })}
      {isHuman && humanData && (
        <div className="human-note">
          Based on {humanData.responses} Arabic speakers' first guesses (no context).
          Bootstrap 90% interval from resampling available on hover.
        </div>
      )}
    </div>
  )
}
