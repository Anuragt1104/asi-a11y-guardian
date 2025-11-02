# A11y Guardian

![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)
![tag:hackathon](https://img.shields.io/badge/hackathon-5F43F1)
![tag:domain/accessibility](https://img.shields.io/badge/accessibility-2E7D32)

Multi-agent autonomous web accessibility auditing for WCAG 2.1/2.2 using uAgents, MeTTa reasoning, and the Chat Protocol. Agents collaborate to fetch, analyze, reason over WCAG knowledge (via MeTTa), and return a prioritized, fix‑oriented report through ASI:One.

## Agents

- Gateway Agent (ASI:One, Chat Protocol): `src/gateway_agent/agent.py`
- Orchestrator Agent (routing): `src/orchestrator_agent/agent.py`
- Fetcher Agent (HTTP + parse): `src/fetcher_agent/agent.py`
- Analyzer Agent (static checks): `src/analyzer_agent/agent.py`
- MeTTa Rules Agent (WCAG mapping): `src/metta_agent/agent.py`, knowledge: `src/metta_agent/knowledge.metta`
- Resource Agent (free references): `src/resource_agent/agent.py`

## Quick Start

### 1. Setup Environment
```bash
# Install dependencies
./scripts/bootstrap.sh

# Create .env from template
cp env.template .env
```

### 2. Run Tests
```bash
source .venv/bin/activate
PYTHONPATH=$PWD pytest tests/ -v
```

### 3. Local Testing
```bash
# Start all agents
./scripts/run_all_agents.sh

# Extract agent addresses
./scripts/extract_addresses.sh

# Copy addresses to .env, then restart main agents
./scripts/restart_main_agents.sh

# Stop all agents
./scripts/stop_all_agents.sh
```

See [LOCAL_TESTING.md](./LOCAL_TESTING.md) for detailed testing instructions.

### 4. Deploy to Agentverse
See [DEPLOYMENT.md](./DEPLOYMENT.md) for step-by-step deployment guide.

## Environment Variables

Create `.env` from `env.template`:

```bash
# Agent Addresses (auto-generated on first run)
ORCHESTRATOR_ADDR=
ORCH_FETCHER_ADDR=
ORCH_ANALYZER_ADDR=
ORCH_METTA_ADDR=
ORCH_RESOURCES_ADDR=

# Agentverse (for deployment)
AGENTVERSE_TOKEN=
MAILBOX_SECRET=
ASI_ONE_API_KEY=

# Optional LLM keys (not currently used)
OPENAI_API_KEY=
CLAUDE_API_KEY=
```

## Testing

### Unit Tests
```bash
source .venv/bin/activate
PYTHONPATH=$PWD pytest tests/ -v
```

### Local Multi-Agent Testing

Use the helper scripts for easy local testing:

```bash
# Start all 6 agents in background
./scripts/run_all_agents.sh

# Wait 5 seconds, then extract addresses
./scripts/extract_addresses.sh

# Copy addresses to .env, then restart
./scripts/restart_main_agents.sh

# Stop all agents when done
./scripts/stop_all_agents.sh
```

Or run manually in separate terminals (see [LOCAL_TESTING.md](./LOCAL_TESTING.md)).

## Using via ASI:One

- Register all agents on Agentverse with `publish_manifest=True`.
- Ensure the Gateway has Chat Protocol enabled and a good README/handles for discoverability.
- In ASI:One chat, send a message like:
```
https://example.com
```
The Gateway will acknowledge and initiate an audit. It replies with a short summary and top 10 issues including fixes and references.

Depth parameter:
- You can pass an optional crawl depth via `AuditRequest.depth` (default 1). The orchestrator audits same‑host links up to that depth and aggregates issues across pages.

## Input/Output Models

See `src/common/models.py` for:
- `AuditRequest` → `AuditReport`
- `FetchContentRequest` → `FetchContentResponse`
- `AnalysisRequest` → `AnalysisResponse`
- `MeTTaQueryRequest` → `MeTTaQueryResponse`
- `ResourceRequest` → `ResourceResponse`




