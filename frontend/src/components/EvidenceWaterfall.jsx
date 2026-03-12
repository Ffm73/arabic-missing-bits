// Implementation: AI generated
export default function EvidenceWaterfall({ analysis }) {
  if (!analysis || !analysis.stages) return null

  const { stages, candidates } = analysis
  const hasM = !!stages.morphology
  const hasC = !!stages.context

  if (!hasM && !hasC) return null

  const sorted = [...candidates].sort((a, b) => b.probability - a.probability)

  const stageList = ['orthography']
  if (hasM) stageList.push('morphology')
  if (hasC) stageList.push('context')

  const stageLabels = {
    orthography: 'Prior',
    morphology: '+ Morph',
    context: '+ Context',
  }

  return (
    <div className="card waterfall-card">
      <div className="wf-header">
        <span className="wf-label">How evidence changed each reading</span>
      </div>

      <div className="wf-table">
        <div className="wf-row wf-header-row">
          <div className="wf-cell wf-reading-cell"></div>
          {stageList.map(s => (
            <div key={s} className="wf-cell wf-stage-cell">{stageLabels[s]}</div>
          ))}
        </div>

        {sorted.map((c, ci) => {
          const idx = candidates.findIndex(x => x.id === c.id)
          return (
            <div key={c.id} className="wf-row">
              <div className="wf-cell wf-reading-cell">
                <span className="wf-translit">{c.transliteration}</span>
                <span className="wf-gloss">{c.gloss}</span>
              </div>
              {stageList.map(s => {
                const p = stages[s]?.probs?.[idx]
                const pct = p != null ? Math.round(p * 100) : '—'
                const isTop = p != null && stageList.indexOf(s) === stageList.length - 1 && ci === 0
                return (
                  <div key={s} className={`wf-cell wf-val-cell ${isTop ? 'wf-top' : ''}`}>
                    <div className="wf-minibar-track">
                      <div
                        className="wf-minibar-fill"
                        style={{ width: p != null ? `${pct}%` : '0%' }}
                      />
                    </div>
                    <span className="wf-pct">{pct}%</span>
                  </div>
                )
              })}
            </div>
          )
        })}

        <div className="wf-row wf-entropy-row">
          <div className="wf-cell wf-reading-cell">
            <span className="wf-translit">Entropy</span>
          </div>
          {stageList.map(s => (
            <div key={s} className="wf-cell wf-val-cell">
              <span className="wf-entropy-val">{stages[s]?.entropy?.toFixed(2)}</span>
              <span className="wf-entropy-unit">bits</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}
