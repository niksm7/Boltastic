# Boltastic MCP Server

MCP server with a single tool: **ui_analysis_tool**. It visits the Nova Web login and home pages, captures screenshots, and uses Google Gemini to analyze the UI and return a summary and possible fix for the given query/issue.

## Tool

- **ui_analysis_tool(query_or_issue: str)**  
  - Visits https://niksm7.github.io/nova-web/login and https://niksm7.github.io/nova-web/
  - Takes full-page screenshots
  - Sends the query/issue and screenshots to Gemini 2.0 Flash
  - Returns: `{ success, error?, summary, possible_fix?, pages_analyzed }`

## Setup (uv)

```bash
# Install uv if needed: https://docs.astral.sh/uv/
uv sync
uv run playwright install chromium
```

## Environment

- **GOOGLE_API_KEY** or **GEMINI_API_KEY** – required for Gemini.
- **PORT** – server port (default 8080).

## Run locally

```bash
export GOOGLE_API_KEY=your-key
uv run mcp_server.py
```

## Run with Docker

```bash
docker build -t boltastic-mcp-server .
docker run -p 8080:8080 -e GOOGLE_API_KEY=your-key boltastic-mcp-server
```

## Deploy to Cloud Run

See `commands.txt` for example `gcloud` build and deploy commands. Set `GOOGLE_API_KEY` (or `GEMINI_API_KEY`) in the Cloud Run service.

## MCP connector (Kibana)

Point the MCP connector at this server’s URL (e.g. `http://localhost:8080` or your Cloud Run URL). The server uses FastMCP with `streamable-http` transport.
