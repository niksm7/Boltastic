import { useRef, useEffect, useState } from 'react'
import { Send, Bot, User, Loader2 } from 'lucide-react'

const API_BASE = 'http://127.0.0.1:8000'
const AGENT_NAME = 'boltastic_agent'
const USER_ID = 'boltastic_web_user'

const LOADING_PHRASES = [
  'Analyzing your request…',
  'Coordinating with agents…',
  'Fetching live data…',
  'Running diagnostics…',
  'Preparing response…',
]

function extractFinalText(events) {
  if (!Array.isArray(events) || events.length === 0) return null
  for (let i = events.length - 1; i >= 0; i--) {
    const evt = events[i]
    const parts = evt?.content?.parts || []
    for (const part of parts) {
      if (part?.text) return part.text
    }
  }
  return null
}

export default function Chat() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [sessionId, setSessionId] = useState(null)
  const [loading, setLoading] = useState(false)
  const [loadingPhraseIndex, setLoadingPhraseIndex] = useState(0)
  const [error, setError] = useState(null)
  const listRef = useRef(null)

  useEffect(() => {
    listRef.current?.scrollTo(0, listRef.current.scrollHeight)
  }, [messages])

  useEffect(() => {
    if (!loading) return
    const interval = setInterval(() => {
      setLoadingPhraseIndex((i) => (i + 1) % LOADING_PHRASES.length)
    }, 2500)
    return () => clearInterval(interval)
  }, [loading])

  async function ensureSession() {
    if (sessionId) return sessionId
    try {
      const res = await fetch(
        `${API_BASE}/apps/${AGENT_NAME}/users/${USER_ID}/sessions`,
        {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ app_name: AGENT_NAME, user_id: USER_ID }),
        }
      )
      if (!res.ok) throw new Error(`Session failed: ${res.status}`)
      const json = await res.json()
      const id = json.id ?? json.session_id
      setSessionId(id)
      return id
    } catch (e) {
      setError('Could not create session. Is the agent API running on :8000?')
      return null
    }
  }

  async function sendMessage() {
    const text = input.trim()
    if (!text || loading) return
    setError(null)
    setInput('')
    setMessages((m) => [...m, { role: 'user', content: text }])
    setLoading(true)

    try {
      const sid = await ensureSession()
      if (!sid) {
        setLoading(false)
        return
      }

      const payload = {
        appName: AGENT_NAME,
        userId: USER_ID,
        sessionId: sid,
        newMessage: {
          role: 'user',
          parts: [{ text }],
        },
      }

      const res = await fetch(`${API_BASE}/run`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(payload),
      })

      if (!res.ok) throw new Error(`Run failed: ${res.status}`)
      const events = await res.json()
      const finalText = extractFinalText(events) || 'No response generated.'
      setMessages((m) => [...m, { role: 'assistant', content: finalText }])
    } catch (e) {
      console.error(e)
      setMessages((m) => [
        ...m,
        { role: 'assistant', content: `Error: ${e.message}. Check the agent API.` },
      ])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="mx-auto flex h-[calc(100vh-4rem)] max-w-4xl flex-col px-4 py-6">
      <div className="mb-4 flex items-center gap-2 border-b border-slate-800/60 pb-3">
        <Bot className="h-5 w-5 text-accent-cyan" />
        <span className="font-mono text-sm text-slate-400">Supervisor Agent (boltastic_agent)</span>
      </div>

      {error && (
        <div className="mb-4 rounded-lg border border-rose-500/40 bg-accent-rose/10 px-4 py-2 text-sm text-rose-300">
          {error}
        </div>
      )}

      <div
        ref={listRef}
        className="flex-1 space-y-4 overflow-y-auto rounded-lg border border-slate-700/60 bg-navy-900/30 p-4"
      >
        {messages.length === 0 && (
          <div className="flex flex-col items-center justify-center py-12 text-center text-slate-500">
            <Bot className="h-12 w-12 text-slate-600" />
            <p className="mt-2 font-mono text-sm">Ask the Supervisor anything.</p>
            <p className="mt-1 text-xs">Sales, Marketing, Engineering—unified intelligence.</p>
          </div>
        )}
        {messages.map((msg, i) => (
          <div
            key={i}
            className={`flex gap-3 ${
              msg.role === 'user' ? 'flex-row-reverse' : ''
            }`}
          >
            <div
              className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-lg ${
                msg.role === 'user'
                  ? 'bg-accent-cyan/20 text-accent-cyan'
                  : 'bg-slate-700/60 text-slate-400'
              }`}
            >
              {msg.role === 'user' ? <User className="h-4 w-4" /> : <Bot className="h-4 w-4" />}
            </div>
            <div
              className={`max-w-[85%] rounded-lg px-3 py-2 ${
                msg.role === 'user'
                  ? 'bg-accent-cyan/15 text-slate-200'
                  : 'bg-navy-800/80 text-slate-300'
              }`}
            >
              <div className="chat-content whitespace-pre-wrap text-sm">{msg.content}</div>
            </div>
          </div>
        ))}
        {loading && (
          <div className="flex gap-3">
            <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-slate-700/60 text-slate-400">
              <Loader2 className="h-4 w-4 animate-spin" />
            </div>
            <div className="flex items-center gap-2 rounded-lg bg-navy-800/80 px-3 py-2 text-sm text-slate-400">
              <span className="inline-block h-2 w-2 animate-pulse rounded-full bg-accent-cyan" />
              {LOADING_PHRASES[loadingPhraseIndex]}
            </div>
          </div>
        )}
      </div>

      <form
        className="mt-4 flex gap-2"
        onSubmit={(e) => {
          e.preventDefault()
          sendMessage()
        }}
      >
        <input
          type="text"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          placeholder="Ask the Supervisor…"
          className="flex-1 rounded-lg border border-slate-700/60 bg-navy-900/80 px-4 py-3 text-sm text-white placeholder-slate-500 focus:border-accent-cyan/50 focus:outline-none focus:ring-1 focus:ring-accent-cyan/50"
          disabled={loading}
        />
        <button
          type="submit"
          disabled={loading || !input.trim()}
          className="rounded-lg bg-accent-cyan px-4 py-3 text-navy-950 hover:bg-accent-cyan/90 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
        >
          <Send className="h-5 w-5" />
        </button>
      </form>
    </div>
  )
}
