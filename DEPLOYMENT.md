# Agentverse Deployment Guide

This guide walks you through deploying the A11y Guardian agents to Agentverse and making them accessible via ASI:One.

## Prerequisites

- All agents tested locally (see [LOCAL_TESTING.md](./LOCAL_TESTING.md))
- Agentverse account at https://agentverse.ai
- Agentverse API token

## Step 1: Get Agentverse API Token

1. Go to https://agentverse.ai and sign in
2. Navigate to **Profile** → **API Keys**
3. Click **Create New Key**
4. Copy the token and add it to your `.env`:

```bash
AGENTVERSE_TOKEN=your_token_here
```

## Step 2: Register Agents on Agentverse

You have two options for deployment:

### Option A: Deploy via Agentverse UI (Recommended for Hackathon)

1. **Login to Agentverse** at https://agentverse.ai

2. **For Each Agent, Create a New Agent:**
   - Click **"Create Agent"** or **"New Agent"**
   - Choose **"Upload Python File"** or **"Paste Code"**

3. **Deploy Agents in This Order:**

#### Agent 1: Fetcher Agent
- **Name:** `a11y_fetcher`
- **File:** `src/fetcher_agent/agent.py`
- **Requirements:** Add in Agentverse:
  ```
  uagents>=0.15,<0.17
  uagents-core==0.3.10
  httpx==0.27.2
  beautifulsoup4==4.12.3
  lxml==5.3.0
  ```
- **Mailbox:** Not required (internal agent)
- **Publish Manifest:** No

#### Agent 2: Analyzer Agent
- **Name:** `a11y_analyzer`
- **File:** `src/analyzer_agent/agent.py`
- **Requirements:**
  ```
  uagents>=0.15,<0.17
  uagents-core==0.3.10
  beautifulsoup4==4.12.3
  lxml==5.3.0
  ```
- **Mailbox:** Not required
- **Publish Manifest:** No

#### Agent 3: MeTTa Agent
- **Name:** `a11y_metta`
- **Files:** 
  - Main: `src/metta_agent/agent.py`
  - Knowledge: `src/metta_agent/knowledge.metta` (upload as asset or paste inline)
- **Requirements:**
  ```
  uagents>=0.15,<0.17
  uagents-core==0.3.10
  hyperon==0.2.8
  ```
- **Note:** Make sure `knowledge.metta` is uploaded and path is correct
- **Mailbox:** Not required
- **Publish Manifest:** No

#### Agent 4: Resource Agent
- **Name:** `a11y_resources`
- **File:** `src/resource_agent/agent.py`
- **Requirements:**
  ```
  uagents>=0.15,<0.17
  uagents-core==0.3.10
  ```
- **Mailbox:** Not required
- **Publish Manifest:** No

#### Agent 5: Orchestrator Agent
- **Name:** `a11y_orchestrator`
- **File:** `src/orchestrator_agent/agent.py`
- **Requirements:**
  ```
  uagents>=0.15,<0.17
  uagents-core==0.3.10
  ```
- **Environment Variables (set in Agentverse):**
  ```
  ORCH_FETCHER_ADDR=<fetcher_agent_address>
  ORCH_ANALYZER_ADDR=<analyzer_agent_address>
  ORCH_METTA_ADDR=<metta_agent_address>
  ORCH_RESOURCES_ADDR=<resource_agent_address>
  ```
- **Mailbox:** Not required
- **Publish Manifest:** No

#### Agent 6: Gateway Agent (Public-Facing)
- **Name:** `a11y_gateway`
- **File:** `src/gateway_agent/agent.py`
- **Requirements:**
  ```
  uagents>=0.15,<0.17
  uagents-core==0.3.10
  ```
- **Environment Variables:**
  ```
  ORCHESTRATOR_ADDR=<orchestrator_agent_address>
  ```
- **Mailbox:** ✅ **ENABLE** (Required for ASI:One communication)
- **Publish Manifest:** ✅ **YES** (Required for Chat Protocol)
- **Description:** "Multi-agent accessibility auditing for WCAG 2.1/2.2. Send a URL to get a comprehensive accessibility report with fixes and references."

### Option B: Deploy via CLI (Advanced)

If you have the Agentverse CLI installed:

```bash
# Login
agentverse login --api-key YOUR_TOKEN

# Deploy each agent
agentverse agent deploy src/fetcher_agent/agent.py --name a11y_fetcher
agentverse agent deploy src/analyzer_agent/agent.py --name a11y_analyzer
agentverse agent deploy src/metta_agent/agent.py --name a11y_metta
agentverse agent deploy src/resource_agent/agent.py --name a11y_resources
agentverse agent deploy src/orchestrator_agent/agent.py --name a11y_orchestrator
agentverse agent deploy src/gateway_agent/agent.py --name a11y_gateway --mailbox --publish-manifest
```

## Step 3: Configure Agent Addresses

After all agents are deployed:

1. **Copy each agent's address** from the Agentverse UI (shown in agent details)
2. **Update environment variables** for Orchestrator and Gateway:

**In Orchestrator Agent Settings:**
```bash
ORCH_FETCHER_ADDR=agent1q...
ORCH_ANALYZER_ADDR=agent1q...
ORCH_METTA_ADDR=agent1q...
ORCH_RESOURCES_ADDR=agent1q...
```

**In Gateway Agent Settings:**
```bash
ORCHESTRATOR_ADDR=agent1q...
```

3. **Restart** the Orchestrator and Gateway agents to pick up the new variables

## Step 4: Enable Chat Protocol for ASI:One

The Gateway agent is already configured with Chat Protocol. Verify it's working:

1. Go to your **Gateway agent** in Agentverse
2. Check that **"Mailbox"** is enabled
3. Verify **"Manifest Published"** shows as ✅
4. Copy the **Agent Address** for testing

## Step 5: Test via ASI:One

### 5.1 Find Your Agent in ASI:One

1. Open https://asi.one or the ASI:One chat interface
2. Search for `a11y_gateway` or your gateway agent name
3. Start a conversation

### 5.2 Send Test Audit Request

In the ASI:One chat, send:

```
https://example.com
```

Expected response:
```
Running accessibility audit for: https://example.com

Audit Summary for https://example.com
Issues: 3
By severity: {'high': 2, 'medium': 1}

1. [high] missing_lang - <html> element is missing a lang attribute.
   Fix: Add a valid lang attribute to the <html> tag, e.g., <html lang="en">.
   Refs: https://www.w3.org/WAI/WCAG21/Understanding/language-of-page/, ...

2. [high] missing_alt - Image is missing meaningful alt text.
   Fix: Provide meaningful alt text describing the image purpose.
   ...
```

### 5.3 Test Multi-Page Audit

The system supports depth parameter (default is 1). To audit linked pages:

```
https://example.com/page depth:2
```

## Step 6: Verify Hackathon Requirements

### ✅ Checklist for Judging

- [ ] All agents registered on Agentverse
- [ ] Gateway has Chat Protocol enabled
- [ ] Gateway is discoverable in ASI:One
- [ ] README.md has Innovation Lab and Hackathon badges
- [ ] Agent names and addresses documented in README.md
- [ ] Agents categorized under "Innovation Lab"
- [ ] Demo video (3-5 min) recorded and uploaded

### Agent Badges in README

Make sure these badges are in your README.md:

```markdown
![tag:innovationlab](https://img.shields.io/badge/innovationlab-3D8BD3)
![tag:hackathon](https://img.shields.io/badge/hackathon-5F43F1)
```

## Step 7: Demo Video (3-5 minutes)

Record a video covering:

1. **Introduction (30s)**
   - Problem: Web accessibility testing is manual and time-consuming
   - Solution: Multi-agent autonomous WCAG auditing

2. **Agentverse Dashboard (1 min)**
   - Show all 6 agents deployed
   - Highlight Chat Protocol on gateway
   - Show agent addresses and configuration

3. **Live Demo via ASI:One (2 min)**
   - Open ASI:One chat
   - Send URL for audit
   - Show real-time processing
   - Display comprehensive report with WCAG mappings, fixes, and references

4. **Code Walkthrough (1 min)**
   - Show MeTTa knowledge graph (`knowledge.metta`)
   - Highlight multi-agent orchestration
   - Explain accessibility checks in analyzer

5. **Conclusion (30s)**
   - Technologies used: uAgents, MeTTa, Chat Protocol
   - Real-world impact: automated WCAG compliance
   - Future enhancements

## Troubleshooting

### Issue: Gateway not discoverable in ASI:One
**Solution:** 
- Ensure mailbox is enabled on gateway
- Verify `publish_manifest=True` in code
- Check agent is running (green status in Agentverse)

### Issue: Orchestrator can't reach sub-agents
**Solution:**
- Verify all agent addresses are correctly set in environment variables
- Check all agents are deployed and running
- Restart orchestrator after updating addresses

### Issue: MeTTa agent fails to load knowledge
**Solution:**
- Ensure `knowledge.metta` is uploaded as an asset
- Verify file path in `agent.py` matches uploaded location
- Check Agentverse logs for file access errors

### Issue: Chat Protocol not working
**Solution:**
- Verify gateway includes `chat_protocol_spec`
- Check that `agent.include(chat_proto, publish_manifest=True)` is called
- Ensure mailbox secret is configured (auto-generated by Agentverse)

## Support & Resources

- **Agentverse Docs:** https://docs.fetch.ai/concepts/agents/
- **uAgents Framework:** https://github.com/fetchai/uAgents
- **ASI Alliance:** https://asi.ai
- **MeTTa Language:** https://github.com/trueagi-io/hyperon-experimental

## Final Notes for Hackathon

- Test thoroughly before submission
- Document any known limitations
- Include setup instructions in README
- Provide clear agent addresses for judges
- Make demo video engaging and concise
- Show real-world use case (test actual websites with accessibility issues)

Good luck with your submission! 🚀

