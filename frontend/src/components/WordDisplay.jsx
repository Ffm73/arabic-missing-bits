// Implementation: AI generated
export default function WordDisplay({
  example,
  analysis,
  currentIndex,
  total,
  onPrev,
  onNext,
  onDotClick,
}) {
  const surface = analysis?.surface_form || example?.surface || ''
  const rootTranslit = analysis?.root_translit || example?.root_translit || ''
  const rootMeaning = analysis?.root_meaning || example?.root_meaning || ''

  return (
    <div className="card word-display">
      <div className="word-nav">
        <button className="nav-btn" onClick={onPrev} aria-label="Previous word">
          &#8592;
        </button>
        <div className="arabic-surface">{surface}</div>
        <button className="nav-btn" onClick={onNext} aria-label="Next word">
          &#8594;
        </button>
      </div>

      <div className="root-info">
        root: <span>{rootTranslit}</span> — {rootMeaning}
      </div>

      <div className="word-dots">
        {Array.from({ length: total }).map((_, i) => (
          <button
            key={i}
            className={`word-dot ${i === currentIndex ? 'active' : ''}`}
            onClick={() => onDotClick(i)}
            aria-label={`Example ${i + 1}`}
          />
        ))}
      </div>
    </div>
  )
}
