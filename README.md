## Boltastic

Boltastic is an AI-powered observability and GTM copilot that connects **Sales**, **Marketing**, and **Engineering** via specialized agents, Elastic Search/Kibana, Salesforce, and a Nova Web frontend.

### Project Structure

- **frontend/**: Nova Web marketing site and supervisor chat UI (React, Vite, Tailwind-style classes).
- **elastic/**:
  - `agent-definitions/`: JSON definitions for Core Tech, Nova (Marketing), and Orbit (Sales) agents.
  - `dashboards/`: Kibana dashboard exports (e.g. billing and cost).
  - `anomaly-jobs/`: ML anomaly detection job templates.
  - `connectors/`: Elastic connector exports.
  - `workflows/`: Elastic automations (e.g. Salesforce SOQL/query + record creation).
- **mcp-server/**: Python MCP server exposing `ui_analysis_tool` to inspect the Nova Web UI via Playwright and Gemini.
- **supervisor/**: Supervisor agent configuration for routing user intent to the right agent.

### Tech Stack

- **Frontend**: React, React Router, Vite, `lucide-react`.
- **AI / Agents**:
  - Google Gemini 2.5 via Google ADK.
  - Agent definitions for Core Tech, Nova (Marketing), Orbit (Sales), and a Boltastic Supervisor.
- **Data / Integrations**:
  - Elasticsearch & Kibana (dashboards, anomaly jobs, ES|QL).
  - Salesforce (playbooks, deal interventions).
  - Jira & Slack (automated tasks/alerts, via agents).
- **Backend / MCP**:
  - Python 3.10+, FastMCP, Playwright, `google-generativeai`, `python-dotenv`.

### Getting Started

#### Prerequisites

- Node.js 18+ and npm (for `frontend`).
- Python 3.10+ and `pip` (for MCP server and scripts).
- An Elastic Cloud deployment (or self-managed cluster) with Kibana access.
- Salesforce/Jira/Slack access if you plan to wire up full automations.
- A Gemini API key (`GOOGLE_API_KEY` or `GEMINI_API_KEY`).

#### Frontend (Nova Web + Supervisor UI)

1. Change into the frontend directory:

   ```bash
   cd frontend
   ```

2. Install dependencies:

   ```bash
   npm install
   ```

3. Start the dev server:

   ```bash
   npm run dev
   ```

4. Open the URL printed in the terminal and use:

- `Home` page: overview of agents, telemetry, and integrations.
- `Chat` page: supervisor chat experience that routes requests to Core/Nova/Orbit agents.
- `Dashboard` link: deep link into Kibana dashboards.

#### MCP Server (`ui_analysis_tool`)

1. Create and activate a virtual environment (recommended):

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```

2. Install Python dependencies:

   ```bash
   pip install -r requirements.txt
   pip install fastmcp google-generativeai playwright python-dotenv
   playwright install chromium
   ```

3. Configure environment variables (for local dev):

   ```bash
   cd mcp-server
   cp ../mcp-server/env_example .env  # if provided, otherwise create .env
   ```

   Ensure `.env` contains at least:

   ```bash
   GOOGLE_API_KEY=your_gemini_api_key
   PORT=8080
   ```

4. Run the MCP server:

   ```bash
   python mcp_server.py
   ```

The `ui_analysis_tool` will:

- Open the Nova Web login and home pages (hosted at `https://niksm7.github.io/nova-web`).
- Capture screenshots via Playwright.
- Send the screenshots plus your issue description to Gemini for analysis.
- Return a concise UI summary and suggested fix.

### Elastic Content

- **Dashboards** (`elastic/dashboards/*.ndjson`): import into Kibana to get prebuilt views for revenue, cost, and GTM performance.
- **Anomaly Jobs** (`elastic/anomaly-jobs/*.json`): ML jobs and datafeed templates to detect positive/negative anomalies across campaigns, revenue, and usage.
- **Connectors** (`elastic/connectors/*.ndjson`): connector exports (e.g., for Slack/Jira/Email).
- **Workflows** (`elastic/workflows/*.yaml`): Elastic workflows for Salesforce SOQL queries and record creation, used by Nova/Orbit style agents.

### Agents Overview

- **Core Tech Agent** (`boltastic-core-agent`):
  - Full-stack debugging specialist for the Nova Web app.
  - Bridges Elastic telemetry, Playwright UI analysis (`ui_analysis_tool`), and GitHub source code.
  - Enforces a "surgical changes only" rule when proposing fixes and PRs.

- **Nova Agent (Marketing)** (`boltastic-nova-agent`):
  - Monitors campaign metrics and social sentiment via ES|QL.
  - Uses ML anomalies (`.ml-anomalies-*`) to find both negative dips and positive growth opportunities.
  - Can create Jira tasks and Slack alerts for scaling campaigns (with human confirmation).

- **Orbit Agent (Sales)** (`boltastic-orbit-agent`):
  - Scans Salesforce opportunity pipelines and CRM activities.
  - Aligns risks with official `sales_playbooks__c` strategies via SOQL.
  - Creates `deal_interventions__c` records in Salesforce for high-priority deals (with human-in-the-loop approval).

- **Boltastic Supervisor**:
  - Routes user requests to the most appropriate agent (Core, Nova, Orbit).
  - Manages cross-agent workflows for GTM and engineering teams.

### Development Workflow

- **Frontend**:
  - Implement new pages/components in `frontend/src`.
  - Keep UI changes minimal and well-scoped to preserve the visual debugging assumptions used by the agents.

- **Agents & Elastic**:
  - Update `elastic/agent-definitions/*` when changing agent behavior or tools.
  - Version and export Elastic dashboards, anomaly jobs, connectors, and workflows into the respective folders.

- **MCP / Tooling**:
  - Extend `mcp_server.py` with additional tools if you need more UI or browser-level analysis.
  - Use environment variables for secrets; never commit keys to source control.


