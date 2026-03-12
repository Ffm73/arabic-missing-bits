// Implementation: AI generated
export default function TogglePanel({
  useMorphology,
  useContext,
  contextId,
  contexts,
  contextUsed,
  onMorphologyChange,
  onContextChange,
  onContextIdChange,
  onReset,
  canReset,
  sentenceMode = false,
  disabled = false,
}) {
  return (
    <div className={`card toggle-card ${disabled ? 'toggle-card-disabled' : ''}`}>
      <div className="toggle-header-row">
        <span className="toggle-section-label">Conditional probability updates</span>
        {canReset && !disabled && (
          <button className="reset-btn" onClick={onReset}>
            Reset
          </button>
        )}
      </div>
      {disabled && (
        <p className="toggle-disabled-hint">Only in Model Reasoning mode</p>
      )}

      <label className={`toggle-row ${disabled ? 'toggle-row-disabled' : ''}`}>
        <span className="toggle-label-text" title="Bayesian update: P(reading | morphology) ∝ P(reading) × P(pattern | reading)">
          Morphology
        </span>
        <div className="toggle-switch">
          <input
            type="checkbox"
            checked={useMorphology}
            onChange={(e) => !disabled && onMorphologyChange(e.target.checked)}
            disabled={disabled}
          />
          <span className="toggle-slider" />
        </div>
        <span className="toggle-hint">P(pattern | reading)</span>
      </label>

      <label className={`toggle-row ${disabled ? 'toggle-row-disabled' : ''}`}>
        <span className="toggle-label-text" title="Bayesian update: P(reading | context) ∝ P(reading) × P(context | reading)">
          Context
        </span>
        <div className="toggle-switch">
          <input
            type="checkbox"
            checked={useContext}
            onChange={(e) => !disabled && onContextChange(e.target.checked)}
            disabled={disabled}
          />
          <span className="toggle-slider" />
        </div>
        <span className="toggle-hint">
          {sentenceMode ? 'P(sentence | reading)' : 'P(context | reading)'}
        </span>
      </label>

      {!sentenceMode && (
        <div className={`context-selector ${useContext ? '' : 'hidden'}`}>
          {contexts.length > 1 && (
            <select
              className="context-select"
              value={contextId || ''}
              onChange={(e) => onContextIdChange(e.target.value)}
            >
              {contexts.map((ctx) => (
                <option key={ctx.id} value={ctx.id}>
                  {ctx.sentence_en}
                </option>
              ))}
            </select>
          )}

          {contextUsed && (
            <div className="context-sentence">
              <div className="context-sentence-ar">{contextUsed.sentence_ar}</div>
              <div className="context-sentence-en">{contextUsed.sentence_en}</div>
            </div>
          )}
        </div>
      )}

      {sentenceMode && useContext && contextUsed && (
        <div className="context-sentence">
          <div className="context-sentence-ar">{contextUsed.sentence_ar}</div>
          <div className="context-sentence-en">{contextUsed.sentence_en}</div>
        </div>
      )}
    </div>
  )
}
