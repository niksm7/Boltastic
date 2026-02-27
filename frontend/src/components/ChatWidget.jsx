import { useState } from 'react'
import { Link } from 'react-router-dom'
import { MessageSquare, X } from 'lucide-react'

export default function ChatWidget() {
  const [open, setOpen] = useState(false)

  return (
    <>
      <button
        type="button"
        onClick={() => setOpen(true)}
        className="fixed bottom-6 right-6 z-40 flex h-14 w-14 items-center justify-center rounded-full bg-accent-cyan text-navy-950 shadow-lg hover:bg-accent-cyan/90 transition-colors"
        aria-label="Open Supervisor chat"
      >
        <MessageSquare className="h-6 w-6" />
      </button>

      {open && (
        <div className="fixed inset-0 z-50 flex items-end justify-end p-4 sm:p-6">
          <div
            className="absolute inset-0 bg-black/50"
            aria-hidden
            onClick={() => setOpen(false)}
          />
          <div className="relative w-full max-w-md overflow-hidden rounded-xl border border-slate-700/60 bg-navy-900 shadow-2xl">
            <div className="flex items-center justify-between border-b border-slate-700/60 bg-navy-800/80 px-4 py-3">
              <span className="font-mono text-sm font-medium text-slate-300">
                Supervisor Agent (A2A)
              </span>
              <button
                type="button"
                onClick={() => setOpen(false)}
                className="rounded p-1 text-slate-400 hover:bg-navy-700 hover:text-white"
                aria-label="Close"
              >
                <X className="h-5 w-5" />
              </button>
            </div>
            <div className="flex flex-col items-center justify-center gap-3 px-4 py-8 text-center">
              <MessageSquare className="h-10 w-10 text-slate-600" />
              <p className="text-sm text-slate-400">
                Open the full chat to talk to the Supervisor.
              </p>
              <Link
                to="/chat"
                onClick={() => setOpen(false)}
                className="rounded-lg bg-accent-cyan/20 px-4 py-2 text-sm font-medium text-accent-cyan hover:bg-accent-cyan/30"
              >
                Go to Chat
              </Link>
            </div>
          </div>
        </div>
      )}
    </>
  )
}
