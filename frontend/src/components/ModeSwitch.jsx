// Implementation: AI generated
export default function ModeSwitch({ mode, onModeChange }) {
  return (
    <div className="mode-switch">
      <button
        className={`mode-btn ${mode === 'curated' ? 'active' : ''}`}
        onClick={() => onModeChange('curated')}
      >
        Curated Demo
      </button>
      <button
        className={`mode-btn ${mode === 'sentence' ? 'active' : ''}`}
        onClick={() => onModeChange('sentence')}
      >
        Try a Sentence
      </button>
    </div>
  )
}
