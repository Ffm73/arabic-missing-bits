// Implementation: AI generated
import { useState } from 'react'

const API = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
  ? 'http://127.0.0.1:8000'
  : ''

export default function SentenceInput({ onWordSelected, selectedExampleId }) {
  const [sentence, setSentence] = useState('')
  const [scanResult, setScanResult] = useState(null)
  const [scanning, setScanning] = useState(false)

  const handleAnalyze = async () => {
    if (!sentence.trim()) return
    setScanning(true)

    try {
      const res = await fetch(`${API}/scan_sentence`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ sentence: sentence.trim() }),
      })
      const data = await res.json()
      setScanResult(data)

      if (data.detected_words.length === 1) {
        onWordSelected(data.detected_words[0].example_id, sentence.trim())
      }
    } catch (err) {
      console.error('Scan failed:', err)
    } finally {
      setScanning(false)
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter') handleAnalyze()
  }

  const handleWordClick = (word) => {
    onWordSelected(word.example_id, sentence.trim())
  }

  const handleSuggestionClick = (s) => {
    setSentence(s)
    setScanResult(null)
  }

  const renderHighlightedSentence = () => {
    if (!scanResult || !scanResult.detected_words.length) return null

    const s = scanResult.sentence
    const words = scanResult.detected_words.sort((a, b) => a.start - b.start)
    const parts = []
    let cursor = 0

    for (const word of words) {
      if (word.start > cursor) {
        parts.push({ text: s.slice(cursor, word.start), type: 'plain' })
      }
      parts.push({
        text: s.slice(word.start, word.end),
        type: 'highlight',
        word,
      })
      cursor = word.end
    }
    if (cursor < s.length) {
      parts.push({ text: s.slice(cursor), type: 'plain' })
    }

    return (
      <div className="highlighted-sentence" dir="rtl">
        {parts.map((part, i) =>
          part.type === 'highlight' ? (
            <span
              key={i}
              className={`highlight-word ${selectedExampleId === part.word.example_id ? 'selected' : ''}`}
              onClick={() => handleWordClick(part.word)}
              title="Click to analyze this word"
            >
              {part.text}
            </span>
          ) : (
            <span key={i}>{part.text}</span>
          )
        )}
      </div>
    )
  }

  const noMatch = scanResult && scanResult.detected_words.length === 0

  return (
    <div className="card sentence-card">
      <div className="sentence-input-row">
        <input
          className="sentence-input"
          type="text"
          dir="rtl"
          value={sentence}
          onChange={(e) => { setSentence(e.target.value); setScanResult(null) }}
          onKeyDown={handleKeyDown}
          placeholder="اكتب جملة عربية هنا..."
        />
        <button
          className="analyze-btn"
          onClick={handleAnalyze}
          disabled={scanning || !sentence.trim()}
        >
          {scanning ? '...' : 'Analyze'}
        </button>
      </div>

      {scanResult && scanResult.detected_words.length > 0 && (
        <div className="sentence-result">
          {renderHighlightedSentence()}
          <p className="sentence-hint">
            {scanResult.detected_words.length === 1
              ? 'Ambiguous word detected and selected.'
              : 'Click a highlighted word to analyze its readings.'}
          </p>
        </div>
      )}

      {noMatch && (
        <div className="sentence-fallback">
          <p className="fallback-msg">
            No supported ambiguous word found in this sentence.
          </p>
          <p className="fallback-hint">Try one of these:</p>
          <div className="suggested-sentences">
            {scanResult.suggested_sentences.map((s, i) => (
              <button
                key={i}
                className="suggestion-btn"
                dir="rtl"
                onClick={() => handleSuggestionClick(s)}
              >
                {s}
              </button>
            ))}
          </div>
        </div>
      )}

      {!scanResult && (
        <p className="sentence-prompt">
          Type or paste a short Arabic sentence, then click Analyze.
        </p>
      )}
    </div>
  )
}
