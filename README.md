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

## Local Setup

1) Python 3.11
2) Create env and install pinned deps
```
./scripts/bootstrap.sh
```

3) Copy `.env.sample` to `.env` and fill later (optional for local dev):
```
AGENTVERSE_TOKEN=
MAILBOX_SECRET=
ASI_ONE_API_KEY=
OPENAI_API_KEY=
CLAUDE_API_KEY=
ORCHESTRATOR_ADDR=
ORCH_FETCHER_ADDR=
ORCH_ANALYZER_ADDR=
ORCH_METTA_ADDR=
ORCH_RESOURCES_ADDR=
```

Where to add credentials later:
- Place them in `.env` (same keys as above). They are loaded by `src/common/settings.py`.
- On Agentverse, you can set Mailbox secret and publish the manifest; the agent code is already `mailbox=True` on the Gateway.

## Run locally (mailbox agents)

Open separate terminals, activate venv (`. .venv/bin/activate`), then run each:

```
python -m src.fetcher_agent.agent
python -m src.analyzer_agent.agent
python -m src.metta_agent.agent
python -m src.resource_agent.agent
python -m src.orchestrator_agent.agent
python -m src.gateway_agent.agent
```

After the Fetcher/Analyzer/MeTTa/Resource agents start, set their addresses in the Orchestrator and Gateway via Agentverse (preferred) or direct code changes. For hackathon judging, publish manifests for all agents in Agentverse; enable Chat Protocol on the Gateway so ASI:One can reach it.

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

## Notes

- This repo is scaffolded for local development; you can create a new GitHub repo and push this code as-is. The `.env.sample` shows all credentials you’ll add later.
- All external calls use free resources (HTTP, MDN, W3C/WAI). No paid APIs are required.
- Extend `knowledge.metta` for more WCAG mappings (e.g., contrast, focus order, keyboard traps) and refine analyzer rules.

## Demo

Record a 3–5 min walkthrough:
1) Start agents (mailbox), show Agentverse manifests.
2) In ASI:One, input a URL. Show logs across agents.
3) Show summarized report and fixes.
4) Brief code tour (Chat Protocol handler, MeTTa mapping).

