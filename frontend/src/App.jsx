// Implementation: AI generated
import { useState, useEffect, useCallback } from 'react'
import ModeSwitch from './components/ModeSwitch'
import WordDisplay from './components/WordDisplay'
import SentenceInput from './components/SentenceInput'
import CandidateList from './components/CandidateList'
import EntropyMeter from './components/EntropyMeter'
import TogglePanel from './components/TogglePanel'
import ExplanationBox from './components/ExplanationBox'

const API = window.location.hostname === 'localhost' || window.location.hostname === '127.0.0.1'
  ? 'http://127.0.0.1:8000'
  : ''

export default function App() {
  const [mode, setMode] = useState('curated')
  const [examples, setExamples] = useState([])
  const [currentIndex, setCurrentIndex] = useState(0)
  const [useMorphology, setUseMorphology] = useState(false)
  const [useContext, setUseContext] = useState(false)
  const [contextId, setContextId] = useState(null)
  const [analysis, setAnalysis] = useState(null)
  const [loading, setLoading] = useState(true)

  // Sentence mode state
  const [sentenceExampleId, setSentenceExampleId] = useState(null)
  const [sentenceText, setSentenceText] = useState('')

  useEffect(() => {
    fetch(`${API}/examples`)
      .then(res => res.json())
      .then(data => {
        setExamples(data)
        setLoading(false)
      })
      .catch(() => setLoading(false))
  }, [])

  const currentExample = examples[currentIndex] || null

  // ── Curated mode analysis ──
  const runCuratedAnalysis = useCallback(async () => {
    if (!currentExample || mode !== 'curated') return

    const body = {
      example_id: currentExample.id,
      use_morphology: useMorphology,
      use_context: useContext,
      context_id: contextId,
    }

    try {
      const res = await fetch(`${API}/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      })
      setAnalysis(await res.json())
    } catch (err) {
      console.error('Analysis failed:', err)
    }
  }, [currentExample, useMorphology, useContext, contextId, mode])

  useEffect(() => {
    if (mode === 'curated' && currentExample) {
      runCuratedAnalysis()
    }
  }, [currentExample, runCuratedAnalysis, mode])

  // ── Sentence mode analysis ──
  const runSentenceAnalysis = useCallback(async () => {
    if (!sentenceExampleId || !sentenceText || mode !== 'sentence') return

    const body = {
      sentence: sentenceText,
      example_id: sentenceExampleId,
      use_morphology: useMorphology,
      use_context: useContext,
    }

    try {
      const res = await fetch(`${API}/analyze_sentence`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(body),
      })
      setAnalysis(await res.json())
    } catch (err) {
      console.error('Sentence analysis failed:', err)
    }
  }, [sentenceExampleId, sentenceText, useMorphology, useContext, mode])

  useEffect(() => {
    if (mode === 'sentence' && sentenceExampleId) {
      runSentenceAnalysis()
    }
  }, [sentenceExampleId, runSentenceAnalysis, mode, useMorphology, useContext])

  // ── Handlers ──
  const handleModeChange = (newMode) => {
    setMode(newMode)
    setUseMorphology(false)
    setUseContext(false)
    setContextId(null)
    if (newMode === 'sentence') {
      setAnalysis(null)
      setSentenceExampleId(null)
    }
  }

  const handleWordChange = (newIndex) => {
    setCurrentIndex(newIndex)
    setUseMorphology(false)
    setUseContext(false)
    setContextId(null)
  }

  const handleContextToggle = (checked) => {
    setUseContext(checked)
    if (mode === 'curated') {
      if (checked && !contextId && currentExample?.contexts?.length > 0) {
        setContextId(currentExample.contexts[0].id)
      }
      if (!checked) setContextId(null)
    }
  }

  const handleReset = () => {
    setUseMorphology(false)
    setUseContext(false)
    setContextId(null)
  }

  const handleSentenceWordSelected = (exampleId, sentence) => {
    setSentenceExampleId(exampleId)
    setSentenceText(sentence)
  }

  const currentStage = useMorphology && useContext ? 'context'
    : useMorphology ? 'morphology'
    : useContext ? 'context'
    : 'orthography'

  const showAnalysis = mode === 'curated' || (mode === 'sentence' && sentenceExampleId)
  const activeContexts = mode === 'curated' ? (currentExample?.contexts || []) : []

  if (loading) {
    return <div className="loading">Loading examples...</div>
  }

  if (examples.length === 0) {
    return <div className="loading">Could not load data. Is the backend running?</div>
  }

  return (
    <div className="app">
      <header className="header">
        <h1>The Missing Bits of Arabic</h1>
        <p className="subtitle">Modeling how readers resolve ambiguity — a CS109 exploration</p>
      </header>

      <ModeSwitch mode={mode} onModeChange={handleModeChange} />

      {mode === 'curated' && (
        <WordDisplay
          example={currentExample}
          analysis={analysis}
          currentIndex={currentIndex}
          total={examples.length}
          onPrev={() => handleWordChange((currentIndex - 1 + examples.length) % examples.length)}
          onNext={() => handleWordChange((currentIndex + 1) % examples.length)}
          onDotClick={handleWordChange}
        />
      )}

      {mode === 'sentence' && (
        <SentenceInput
          onWordSelected={handleSentenceWordSelected}
          selectedExampleId={sentenceExampleId}
        />
      )}

      {mode === 'sentence' && analysis && (
        <div className="card word-display sentence-selected-word">
          <div className="arabic-surface">{analysis.surface_form}</div>
          <div className="root-info">
            root: <span>{analysis.root_translit}</span> — {analysis.root_meaning}
          </div>
        </div>
      )}

      {showAnalysis && (
        <TogglePanel
          useMorphology={useMorphology}
          useContext={useContext}
          contextId={contextId}
          contexts={activeContexts}
          contextUsed={analysis?.stages?.context?.context_used}
          onMorphologyChange={setUseMorphology}
          onContextChange={handleContextToggle}
          onContextIdChange={setContextId}
          onReset={handleReset}
          canReset={useMorphology || useContext}
          sentenceMode={mode === 'sentence'}
        />
      )}

      {showAnalysis && <CandidateList analysis={analysis} />}

      {showAnalysis && <EntropyMeter analysis={analysis} stage={currentStage} />}

      {showAnalysis && <ExplanationBox analysis={analysis} stage={currentStage} />}

      <footer className="footer">
        CS109 — Probability for Computer Scientists
      </footer>
    </div>
  )
}
