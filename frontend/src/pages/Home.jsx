import { Link } from 'react-router-dom'
import {
  Cpu,
  Megaphone,
  TrendingUp,
  LayoutDashboard,
  MessageSquare,
  ArrowRight,
  Zap,
} from 'lucide-react'

const agents = [
  {
    icon: Cpu,
    title: 'Core Tech Agent',
    description:
      'Full-stack debugging surgeon. Autonomously analyzes frontend/backend errors, fetches GitHub code, creates surgical PRs, and triggers Jira/Slack alerts.',
    color: 'text-accent-cyan',
    bg: 'bg-accent-cyan/10',
  },
  {
    icon: Megaphone,
    title: 'Nova Agent (Marketing)',
    description:
      'Marketing Intelligence. Monitors campaign CTR and social sentiment anomalies. Detects growth opportunities and scales high-performing ads.',
    color: 'text-accent-emerald',
    bg: 'bg-accent-emerald/10',
  },
  {
    icon: TrendingUp,
    title: 'Orbit Agent (Sales)',
    description:
      'Sales Intelligence. Scans Salesforce pipelines for stalled deals, queries live playbooks for strategy, and drafts management interventions.',
    color: 'text-amber-400',
    bg: 'bg-amber-400/10',
  },
  {
    icon: LayoutDashboard,
    title: 'Boltastic Supervisor',
    description:
      'Boltastic supervisor agent intelligently navigates the users request to the most suitable agent.',
    color: 'text-accent-rose',
    bg: 'bg-accent-rose/10',
  },
]

const integrations = [
  'Elasticsearch',
  'Kibana',
  'Salesforce',
  'GitHub',
  'Jira',
  'Slack',
  'Google Gemini',
]

export default function Home() {
  const dashboardOverviewSrc = new URL('../../dashboard_overview.png', import.meta.url).href

  return (
    <>
      {/* Hero */}
      <section className="relative overflow-hidden border-b border-slate-800/60">
        <div className="absolute inset-0 bg-gradient-to-b from-accent-cyan/5 via-transparent to-transparent" />
        <div className="relative mx-auto max-w-7xl px-4 py-16 sm:px-6 lg:px-8 lg:py-24">
          <div className="text-center">
            <h1 className="text-4xl font-bold tracking-tight text-white sm:text-5xl lg:text-6xl">
              Your Enterprise, Autonomously Optimized.
            </h1>
            <p className="mx-auto mt-4 max-w-2xl text-lg text-slate-400">
              Boltastic unites Sales, Marketing, and Engineering through specialized AI agents that
              don&apos;t just report data—they take action.
            </p>
            <div className="mt-8 flex flex-wrap justify-center gap-4">
              <Link
                to="/chat"
                className="inline-flex items-center gap-2 rounded-lg bg-accent-cyan px-5 py-3 text-sm font-medium text-navy-950 hover:bg-accent-cyan/90 transition-colors"
              >
                Launch Supervisor
                <ArrowRight className="h-4 w-4" />
              </Link>
            </div>
          </div>
          {/* Mock chat preview */}
          <div className="mx-auto mt-12 max-w-2xl">
            <div className="rounded-xl border border-slate-700/60 bg-navy-900/80 p-4 shadow-xl ring-1 ring-slate-700/40">
              <div className="flex items-center gap-2 border-b border-slate-700/60 pb-3">
                <MessageSquare className="h-5 w-5 text-accent-cyan" />
                <span className="font-mono text-sm text-slate-400">Supervisor Agent (A2A)</span>
              </div>
              <div className="mt-3 space-y-3 font-mono text-sm">
                <div className="rounded-lg bg-navy-800/80 px-3 py-2 text-slate-300">
                  <span className="text-accent-cyan">User:</span> Summarize pipeline risk and
                  suggest top 3 actions.
                </div>
                <div className="rounded-lg bg-navy-800/80 px-3 py-2 text-slate-400">
                  <span className="text-accent-emerald">Supervisor:</span> Delegating to Orbit &
                  Nova. Fetching pipeline and campaign data…
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* Agent Ecosystem */}
      <section className="border-b border-slate-800/60 py-16 lg:py-20">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <h2 className="text-2xl font-bold text-white sm:text-3xl">Agent Ecosystem</h2>
          <p className="mt-2 text-slate-400">
            Specialized AI agents powered by Google ADK and Gemini 2.5 Pro.
          </p>
          <div className="mt-10 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            {agents.map((agent) => {
              const Icon = agent.icon
              return (
                <div
                  key={agent.title}
                  className="rounded-xl border border-slate-700/60 bg-navy-900/50 p-5 transition-colors hover:border-slate-600/60 hover:bg-navy-800/50"
                >
                  <div
                    className={`inline-flex rounded-lg p-2 ${agent.bg} ${agent.color}`}
                    aria-hidden
                  >
                    <Icon className="h-6 w-6" />
                  </div>
                  <h3 className="mt-3 font-semibold text-white">{agent.title}</h3>
                  <p className="mt-2 text-sm text-slate-400 leading-relaxed">{agent.description}</p>
                </div>
              )
            })}
          </div>
        </div>
      </section>

      {/* Live Dashboard Preview */}
      <section className="border-b border-slate-800/60 py-16 lg:py-20">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <h2 className="text-2xl font-bold text-white sm:text-3xl">
            Real-Time Telemetry & Insights
          </h2>
          <p className="mt-2 text-slate-400">
            Zenith Agent dashboards: Revenue Trend, Cost by Service, Revenue vs Cost.
          </p>
          <div className="mt-8 aspect-video w-full overflow-hidden rounded-xl border-2 border-slate-700/60 bg-navy-900/50 shadow-lg ring-2 ring-accent-cyan/20 animate-glow">
            <img
              src={dashboardOverviewSrc}
              alt="Boltastic dashboard overview"
              className="h-full w-full object-cover"
              loading="lazy"
            />
          </div>
        </div>
      </section>

      {/* Integrations */}
      <section className="py-16 lg:py-20">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <h2 className="text-center text-xl font-semibold text-slate-400">
            Integrated with your stack
          </h2>
          <div className="mt-8 flex flex-wrap justify-center gap-8 overflow-hidden">
            {integrations.map((name) => (
              <span
                key={name}
                className="font-mono text-sm text-slate-500 hover:text-slate-300 transition-colors"
              >
                {name}
              </span>
            ))}
          </div>
        </div>
      </section>
    </>
  )
}
