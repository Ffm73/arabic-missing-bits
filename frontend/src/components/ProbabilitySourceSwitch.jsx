// Implementation: AI generated
export default function ProbabilitySourceSwitch({ source, onSourceChange, humanAvailable }) {
  return (
    <div className="probability-source-switch">
      <span className="probability-source-label">Probability source</span>
      <div className="probability-source-buttons">
        <button
          type="button"
          className={`probability-source-btn ${source === 'human' ? 'active' : ''}`}
          onClick={() => onSourceChange('human')}
          disabled={!humanAvailable}
          title={humanAvailable ? 'Show human first-guess distribution' : 'No human data for this word'}
        >
          Human Intuition
        </button>
        <button
          type="button"
          className={`probability-source-btn ${source === 'model' ? 'active' : ''}`}
          onClick={() => onSourceChange('model')}
          title="Show model distribution (prior + optional morphology & context)"
        >
          Model Reasoning
        </button>
      </div>
    </div>
  )
}
