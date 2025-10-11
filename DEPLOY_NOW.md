# 🚀 Deploy to Agentverse NOW - Quick Guide

## Before You Start
- [ ] You have an Agentverse account: https://agentverse.ai
- [ ] You're logged into Agentverse
- [ ] You have 15-20 minutes

## Deployment Steps

### 📝 Track Your Addresses
As you deploy each agent, **write down its address** in this format:

```
Agent 1 (Fetcher):  agent1q_____________________________
Agent 2 (Analyzer): agent1q_____________________________
Agent 3 (MeTTa):    agent1q_____________________________
Agent 4 (Resource): agent1q_____________________________
Agent 5 (Orchestrator): agent1q_________________________
Agent 6 (Gateway):  agent1q_____________________________
```

---

## Agent 1: Fetcher 🌐
1. Go to https://agentverse.ai/agents
2. Click **"Create Agent"** → **"Blank"**
3. Name: `a11y_fetcher`
4. Copy/paste file: `src/fetcher_agent/agent.py`
5. Add requirements:
   ```
   uagents>=0.15,<0.17
   uagents-core==0.3.10
   httpx==0.27.2
   beautifulsoup4==4.12.3
   lxml==5.3.0
   ```
6. **Deploy** → Copy agent address
7. Write it down!

---

## Agent 2: Analyzer 🔍
1. Create new agent
2. Name: `a11y_analyzer`
3. Copy/paste: `src/analyzer_agent/agent.py`
4. Requirements:
   ```
   uagents>=0.15,<0.17
   uagents-core==0.3.10
   beautifulsoup4==4.12.3
   lxml==5.3.0
   ```
5. Deploy → Copy address

---

## Agent 3: MeTTa 🧠
⚠️ **Special:** This agent needs the knowledge file

**Option A: If file upload works**
- Upload both `agent.py` AND `knowledge.metta`

**Option B: Use inline version (recommended)**
- Use `src/metta_agent/agent_inline_knowledge.py` instead
- This has knowledge embedded in the code

1. Create new agent
2. Name: `a11y_metta`
3. Copy/paste: `src/metta_agent/agent_inline_knowledge.py`
4. Requirements:
   ```
   uagents>=0.15,<0.17
   uagents-core==0.3.10
   hyperon==0.2.8
   ```
5. Deploy → Copy address

---

## Agent 4: Resource 📚
1. Create new agent
2. Name: `a11y_resources`
3. Copy/paste: `src/resource_agent/agent.py`
4. Requirements:
   ```
   uagents>=0.15,<0.17
   uagents-core==0.3.10
   ```
5. Deploy → Copy address

---

## Agent 5: Orchestrator 🎯
⚠️ **Important:** Set environment variables!

1. Create new agent
2. Name: `a11y_orchestrator`
3. Copy/paste: `src/orchestrator_agent/agent.py`
4. Requirements:
   ```
   uagents>=0.15,<0.17
   uagents-core==0.3.10
   ```
5. **Before deploying:** Go to **Settings** or **Environment Variables**
6. Add these 4 variables with addresses from above:
   ```
   ORCH_FETCHER_ADDR=<agent1_address>
   ORCH_ANALYZER_ADDR=<agent2_address>
   ORCH_METTA_ADDR=<agent3_address>
   ORCH_RESOURCES_ADDR=<agent4_address>
   ```
7. Deploy → Copy address

---

## Agent 6: Gateway 🚪
⚠️ **Most Important:** This is your public agent!

1. Create new agent
2. Name: `a11y_gateway`
3. Copy/paste: `src/gateway_agent/agent.py`
4. Requirements:
   ```
   uagents>=0.15,<0.17
   uagents-core==0.3.10
   ```
5. Add environment variable:
   ```
   ORCHESTRATOR_ADDR=<agent5_address>
   ```
6. ✅ **Enable Mailbox** (checkbox/toggle)
7. ✅ **Publish Manifest** (checkbox/toggle)
8. Add description:
   ```
   Multi-agent web accessibility auditor for WCAG 2.1/2.2. 
   Send a URL to get a comprehensive accessibility report.
   ```
9. Deploy → Copy address

---

## ✅ Verify All Agents

Check that all 6 agents show:
- ✅ Green/Running status
- ✅ No errors in logs
- ✅ Gateway has mailbox enabled

---

## 🧪 Test via ASI:One

1. Go to https://asi.one
2. Search for `a11y_gateway`
3. Send message: `https://example.com`
4. Wait for accessibility report!

Expected response:
```
Running accessibility audit for: https://example.com

Audit Summary for https://example.com
Issues: 3
By severity: {'high': 2, 'medium': 1}
...
```

---

## 📹 Record Demo Video

1. Show Agentverse dashboard (all 6 agents)
2. Test live in ASI:One
3. Show code (MeTTa knowledge graph)
4. Explain technologies (uAgents, MeTTa, Chat Protocol)
5. Total: 3-5 minutes

---

## 🎯 Submit to Hackathon

- [ ] All agents deployed ✅
- [ ] ASI:One test successful ✅
- [ ] Demo video recorded ✅
- [ ] README updated with agent addresses ✅
- [ ] GitHub repo public ✅

---

## 📞 Need Help?

Check these files:
- **Detailed Steps:** `AGENTVERSE_DEPLOYMENT_STEPS.md`
- **Requirements:** `AGENT_REQUIREMENTS.md`
- **Troubleshooting:** `DEPLOYMENT.md`

---

**You've got this!** 🚀

Time estimate: 15-20 minutes for full deployment
