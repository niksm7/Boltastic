import { useState } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { Menu, X, Zap } from 'lucide-react'

const navLinks = [
  { to: '/', label: 'Home' },
  { to: '/chat', label: 'Chat' },
  {
    href: 'https://boltastic-project-c0ecb2.kb.us-central1.gcp.elastic.cloud/app/r/s/BPTlh',
    label: 'Dashboard',
    external: true,
  },
]

export default function Navbar() {
  const [open, setOpen] = useState(false)
  const location = useLocation()

  return (
    <header className="sticky top-0 z-50 border-b border-slate-800/60 bg-navy-950/90 backdrop-blur-md">
      <nav className="mx-auto flex max-w-7xl items-center justify-between px-4 py-3 sm:px-6 lg:px-8">
        <Link to="/" className="flex items-center gap-2 text-xl font-bold text-white">
          <Zap className="h-6 w-6 text-accent-cyan" />
          Boltastic
        </Link>

        <div className="hidden md:flex md:items-center md:gap-8">
          {navLinks.map((item) =>
            item.external ? (
              <a
                key={item.label}
                href={item.href}
                target="_blank"
                rel="noopener noreferrer"
                className="text-slate-400 hover:text-white transition-colors"
              >
                {item.label}
              </a>
            ) : (
              <Link
                key={item.label}
                to={item.to}
                className={`transition-colors ${
                  location.pathname === item.to ? 'text-accent-cyan' : 'text-slate-400 hover:text-white'
                }`}
              >
                {item.label}
              </Link>
            )
          )}
          <Link
            to="/chat"
            className="rounded-lg bg-accent-cyan/20 px-4 py-2 text-sm font-medium text-accent-cyan hover:bg-accent-cyan/30 transition-colors"
          >
            Launch Supervisor
          </Link>
        </div>

        <button
          type="button"
          className="md:hidden rounded-lg p-2 text-slate-400 hover:bg-navy-800 hover:text-white"
          onClick={() => setOpen(!open)}
          aria-label="Toggle menu"
        >
          {open ? <X className="h-6 w-6" /> : <Menu className="h-6 w-6" />}
        </button>
      </nav>

      {open && (
        <div className="md:hidden border-t border-slate-800/60 bg-navy-900/95 px-4 py-3">
          <div className="flex flex-col gap-2">
            {navLinks.map((item) =>
              item.external ? (
                <a
                  key={item.label}
                  href={item.href}
                  target="_blank"
                  rel="noopener noreferrer"
                  className="rounded-lg px-3 py-2 text-slate-400 hover:bg-navy-800 hover:text-white"
                  onClick={() => setOpen(false)}
                >
                  {item.label}
                </a>
              ) : (
                <Link
                  key={item.label}
                  to={item.to}
                  className={`rounded-lg px-3 py-2 ${
                    location.pathname === item.to ? 'text-accent-cyan' : 'text-slate-400 hover:text-white'
                  } hover:bg-navy-800`}
                  onClick={() => setOpen(false)}
                >
                  {item.label}
                </Link>
              )
            )}
            <Link
              to="/chat"
              className="rounded-lg bg-accent-cyan/20 px-3 py-2 text-accent-cyan hover:bg-accent-cyan/30"
              onClick={() => setOpen(false)}
            >
              Launch Supervisor
            </Link>
          </div>
        </div>
      )}
    </header>
  )
}
