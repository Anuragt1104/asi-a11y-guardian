# Agent Requirements for Agentverse Deployment

Copy these requirements for each agent when deploying to Agentverse.

## 1. Fetcher Agent
**File:** `src/fetcher_agent/agent.py`

**Requirements:**
```
uagents>=0.15,<0.17
uagents-core==0.3.10
httpx==0.27.2
beautifulsoup4==4.12.3
lxml==5.3.0
```

---

## 2. Analyzer Agent
**File:** `src/analyzer_agent/agent.py`

**Requirements:**
```
uagents>=0.15,<0.17
uagents-core==0.3.10
beautifulsoup4==4.12.3
lxml==5.3.0
```

---

## 3. MeTTa Agent
**Files:** 
- `src/metta_agent/agent.py`
- `src/metta_agent/knowledge.metta` ⚠️ **Must be included**

**Requirements:**
```
uagents>=0.15,<0.17
uagents-core==0.3.10
hyperon==0.2.8
```

⚠️ **Note:** If Agentverse doesn't support file uploads, you'll need to inline the knowledge.metta content.

---

## 4. Resource Agent
**File:** `src/resource_agent/agent.py`

**Requirements:**
```
uagents>=0.15,<0.17
uagents-core==0.3.10
```

---

## 5. Orchestrator Agent
**File:** `src/orchestrator_agent/agent.py`

**Requirements:**
```
uagents>=0.15,<0.17
uagents-core==0.3.10
```

**Environment Variables (Required):**
```bash
ORCH_FETCHER_ADDR=<fetcher_agent_address>
ORCH_ANALYZER_ADDR=<analyzer_agent_address>
ORCH_METTA_ADDR=<metta_agent_address>
ORCH_RESOURCES_ADDR=<resource_agent_address>
```

---

## 6. Gateway Agent  (Public-Facing)
**File:** `src/gateway_agent/agent.py`

**Requirements:**
```
uagents>=0.15,<0.17
uagents-core==0.3.10
```

**Environment Variables (Required):**
```bash
ORCHESTRATOR_ADDR=<orchestrator_agent_address>
```

**Special Configuration:**
- ✅ Enable Mailbox
- ✅ Publish Manifest
- Add Description (for ASI:One discoverability)

---

## Common Models

If Agentverse requires separate files for models, you may need to include:

**File:** `src/common/models.py`

This file is imported by:
- Gateway Agent
- Orchestrator Agent

Most agent frameworks allow imports from the same uploaded files.

---

## Deployment Checklist

- [ ] Fetcher - No env vars needed
- [ ] Analyzer - No env vars needed
- [ ] MeTTa - Include knowledge.metta file
- [ ] Resource - No env vars needed
- [ ] Orchestrator - Set 4 env vars for worker agents
- [ ] Gateway - Set 1 env var for orchestrator, enable mailbox, publish manifest

