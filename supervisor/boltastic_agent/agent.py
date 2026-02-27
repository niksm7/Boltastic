import os
import httpx
from google.adk.agents import LlmAgent
from google.adk.agents.remote_a2a_agent import RemoteA2aAgent
from dotenv import load_dotenv

load_dotenv()

elastic_api_key = os.getenv("ELASTIC_API_KEY")

auth_headers = {
    "Authorization": f"ApiKey {elastic_api_key}",
    "kbn-xsrf": "true",
    "Content-Type": "application/json"
}

shared_client = httpx.AsyncClient(
    headers=auth_headers,
    timeout=300.0 
)

# ---------------------------------------------------------
# 1. Define the Remote Sub-Agents via A2A
# ---------------------------------------------------------
core_agent = RemoteA2aAgent(
    name="boltastic_core_agent",
    description="Senior full-stack debugging specialist focused on the nova-web ecosystem. Fixes bugs, analyzes logs, checks UI, and interacts with GitHub.",
    agent_card="https://boltastic-project-c0ecb2.kb.us-central1.gcp.elastic.cloud/api/agent_builder/a2a/boltastic-core-agent.json",
    httpx_client=shared_client
)

nova_agent = RemoteA2aAgent(
    name="boltastic_nova_agent",
    description="Marketing Intelligence assistant designed to optimize campaign performance and brand sentiment. Handles CTR drops, social sentiment, and ad budgets.",
    agent_card="https://boltastic-project-c0ecb2.kb.us-central1.gcp.elastic.cloud/api/agent_builder/a2a/boltastic-nova-agent.json",
    httpx_client=shared_client
)

orbit_agent = RemoteA2aAgent(
    name="boltastic_orbit_agent",
    description="Sales Intelligence assistant dedicated to managing the sales pipeline and CRM activities. Handles stalled deals, Salesforce playbooks, and interventions.",
    agent_card="https://boltastic-project-c0ecb2.kb.us-central1.gcp.elastic.cloud/api/agent_builder/a2a/boltastic-oribit-agent.json",
    httpx_client=shared_client
)

# ---------------------------------------------------------
# 2. Define the Root Agent for ADK Web
# ---------------------------------------------------------
supervisor_instruction = """
You are the Boltastic Supervisor Agent, the central orchestrator for our AI ecosystem.
Your primary role is to analyze user requests and delegate tasks to the appropriate specialized sub-agents.

Routing Rules:
- If the request involves code, GitHub, UI bugs, or nova-web telemetry, use the 'boltastic_core_agent'.
- If the request involves marketing campaigns, social sentiment, CTR anomalies, or ad opportunities, use the 'boltastic_nova_agent'.
- If the request involves sales pipelines, Salesforce CRM, stalled deals, or playbooks, use the 'boltastic_orbit_agent'.

CRITICAL EXECUTION RULES:
1. NO SUMMARIZATION: You MUST preserve the exact depth, metrics, root cause breakdowns, and detailed recommendations provided by your sub-agents. Do not truncate their hard work into brief summaries.
2. PRESERVE CONTEXT: When you delegate a task to a sub-agent, forward the user's specific context and constraints so the sub-agent knows exactly how deep to go.
3. IN-DEPTH FORMATTING: Present the final synthesized answer comprehensively. Use Markdown headings (e.g., ### Sales Pipeline Analysis), bullet points, and bold text to structure the detailed insights exactly as the sub-agents returned them.
"""

root_agent = LlmAgent(
    name="boltastic_supervisor",
    instruction=supervisor_instruction,
    sub_agents=[core_agent, nova_agent, orbit_agent], 
    model="gemini-2.5-flash" 
)
