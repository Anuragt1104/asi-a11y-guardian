# Agentverse Deployment - Step-by-Step Checklist

## Pre-Deployment Setup ✅

- [x] All tests passing (4/4 tests) ✅
- [ ] Agentverse account created at https://agentverse.ai
- [ ] Agentverse API token added to `.env`
- [ ] Logged into Agentverse dashboard

## Deployment Order (Important!)

Deploy agents in this order so you can configure addresses as you go:

1. Fetcher Agent (no dependencies)
2. Analyzer Agent (no dependencies)
3. MeTTa Agent (no dependencies)
4. Resource Agent (no dependencies)
5. Orchestrator Agent (needs addresses from 1-4)
6. Gateway Agent (needs orchestrator address)

---

## Agent 1: Fetcher Agent 🌐

### File to Upload
- **Main File:** `src/fetcher_agent/agent.py`

### Requirements (Dependencies)
```
uagents>=0.15,<0.17
uagents-core==0.3.10
httpx==0.27.2
beautifulsoup4==4.12.3
lxml==5.3.0
```

### Configuration
- **Agent Name:** `a11y_fetcher`
- **Mailbox:** ❌ Not needed (internal agent)
- **Publish Manifest:** ❌ No
- **Environment Variables:** None

### Steps
1. Go to https://agentverse.ai/agents
2. Click **"Create New Agent"** or **"+"**
3. Choose **"Blank Agent"** or **"Import"**
4. Paste the content of `src/fetcher_agent/agent.py`
5. Add the requirements above in the **"Requirements"** section
6. Click **"Save"** and **"Deploy"**
7. ✅ **IMPORTANT:** Copy the agent address (shows as `agent1q...`)
8. Save it: `ORCH_FETCHER_ADDR=agent1q...`

---

## Agent 2: Analyzer Agent 🔍

### File to Upload
- **Main File:** `src/analyzer_agent/agent.py`

### Requirements
```
uagents>=0.15,<0.17
uagents-core==0.3.10
beautifulsoup4==4.12.3
lxml==5.3.0
```

### Configuration
- **Agent Name:** `a11y_analyzer`
- **Mailbox:** ❌ Not needed
- **Publish Manifest:** ❌ No
- **Environment Variables:** None

### Steps
1. Create new agent in Agentverse
2. Paste `src/analyzer_agent/agent.py`
3. Add requirements
4. Save and Deploy
5. ✅ **Copy address:** `ORCH_ANALYZER_ADDR=agent1q...`

---

## Agent 3: MeTTa Agent 🧠

### Files to Upload
- **Main File:** `src/metta_agent/agent.py`
- **Knowledge File:** `src/metta_agent/knowledge.metta`

### Requirements
```
uagents>=0.15,<0.17
uagents-core==0.3.10
hyperon==0.2.8
```

### Configuration
- **Agent Name:** `a11y_metta`
- **Mailbox:** ❌ Not needed
- **Publish Manifest:** ❌ No
- **Environment Variables:** None

### Steps
1. Create new agent in Agentverse
2. Paste `src/metta_agent/agent.py`
3. **IMPORTANT:** Upload `knowledge.metta` as an additional file/asset
   - If no asset upload option, paste the content directly in the agent code before the `with open(...)` line
4. Add requirements
5. Save and Deploy
6. ✅ **Copy address:** `ORCH_METTA_ADDR=agent1q...`

### Alternative: Inline Knowledge (if file upload doesn't work)
If Agentverse doesn't support file uploads, modify the agent code to include knowledge inline:

```python
# Replace the file reading section with:
knowledge_content = """
(Issue missing_lang)
(SC missing_lang "3.1.1" "Language of Page")
... (paste entire knowledge.metta content here)
"""
metta.run(knowledge_content)
```

---

## Agent 4: Resource Agent 📚

### File to Upload
- **Main File:** `src/resource_agent/agent.py`

### Requirements
```
uagents>=0.15,<0.17
uagents-core==0.3.10
```

### Configuration
- **Agent Name:** `a11y_resources`
- **Mailbox:** ❌ Not needed
- **Publish Manifest:** ❌ No
- **Environment Variables:** None

### Steps
1. Create new agent
2. Paste `src/resource_agent/agent.py`
3. Add requirements
4. Save and Deploy
5. ✅ **Copy address:** `ORCH_RESOURCES_ADDR=agent1q...`

---

## Agent 5: Orchestrator Agent 🎯

**⚠️ IMPORTANT:** Set environment variables with addresses from agents 1-4

### File to Upload
- **Main File:** `src/orchestrator_agent/agent.py`
- **Models File:** `src/common/models.py` (if needed)

### Requirements
```
uagents>=0.15,<0.17
uagents-core==0.3.10
```

### Configuration
- **Agent Name:** `a11y_orchestrator`
- **Mailbox:** ❌ Not needed
- **Publish Manifest:** ❌ No
- **Environment Variables:** ⚠️ **REQUIRED**

### Environment Variables to Set
```bash
ORCH_FETCHER_ADDR=<agent1_address_from_above>
ORCH_ANALYZER_ADDR=<agent2_address_from_above>
ORCH_METTA_ADDR=<agent3_address_from_above>
ORCH_RESOURCES_ADDR=<agent4_address_from_above>
```

### Steps
1. Create new agent
2. Paste `src/orchestrator_agent/agent.py`
3. Add requirements
4. **Go to "Settings" or "Environment Variables"**
5. Add the 4 environment variables with addresses from agents 1-4
6. Save and Deploy
7. ✅ **Copy address:** `ORCHESTRATOR_ADDR=agent1q...`

---

## Agent 6: Gateway Agent 🚪 (Public-Facing)

**⚠️ MOST IMPORTANT:** This is your public-facing agent for ASI:One

### File to Upload
- **Main File:** `src/gateway_agent/agent.py`
- **Models File:** `src/common/models.py` (if needed)

### Requirements
```
uagents>=0.15,<0.17
uagents-core==0.3.10
httpx==0.27.2
```

### Configuration
- **Agent Name:** `a11y_gateway`
- **Mailbox:** ✅ **ENABLE** (Required for ASI:One)
- **Publish Manifest:** ✅ **YES** (Required for Chat Protocol)
- **Environment Variables:** ⚠️ **REQUIRED**

### Environment Variables
```bash
ORCHESTRATOR_ADDR=<orchestrator_address_from_above>
ASI_ONE_API_KEY=<sk_3c365195e8c1492a9af71f53cf77a9e524aa83d53d564b38b27f0b1e3c391a96>
```

### Description (for ASI:One)
```
Multi-agent autonomous web accessibility auditor. Analyzes websites for WCAG 2.1/2.2 compliance. 
Send a URL to get a comprehensive accessibility report with issues, fixes, and W3C/MDN references.

Usage: Send any URL (e.g., https://example.com) to start an audit.
```

### Steps
1. Create new agent
2. Paste `src/gateway_agent/agent.py`
3. Add requirements
4. Add environment variable: `ORCHESTRATOR_ADDR`
5. ✅ **Enable Mailbox** (checkbox or toggle)
6. ✅ **Enable "Publish Manifest"** or **"Make Public"**
7. Add the description above
8. Save and Deploy
9. ✅ **Copy address:** `GATEWAY_ADDR=agent1q...`

---

## Verification Checklist ✅

After all agents are deployed:

### 1. Check All Agents Are Running
- [ ] Fetcher: Green status, no errors
- [ ] Analyzer: Green status, no errors
- [ ] MeTTa: Green status, no errors
- [ ] Resource: Green status, no errors
- [ ] Orchestrator: Green status, environment variables set
- [ ] Gateway: Green status, mailbox enabled, manifest published

### 2. Verify Gateway Configuration
- [ ] Mailbox is enabled (shows mailbox address)
- [ ] Manifest is published (shows "Published" or checkmark)
- [ ] Description is filled in
- [ ] Agent appears in ASI:One search

### 3. Test Communication
- [ ] Check logs in Agentverse for each agent
- [ ] Verify no connection errors
- [ ] Orchestrator shows it found sub-agent addresses

---

## Testing via ASI:One 🧪

### 1. Find Your Agent
1. Go to https://asi.one or open ASI:One app
2. Search for `a11y_gateway` or your gateway agent name
3. Start a conversation

### 2. Send Test Request
Send this message:
```
https://example.com
```

### 3. Expected Response
You should see:
```
Running accessibility audit for: https://example.com

Audit Summary for https://example.com
Issues: 3
By severity: {'high': 2, 'medium': 1}

1. [high] missing_lang - <html> element is missing a lang attribute.
   Fix: Add a valid lang attribute to the <html> tag, e.g., <html lang="en">.
   Refs: https://www.w3.org/WAI/WCAG21/Understanding/language-of-page/
...
```

### 4. Test Multi-Page Audit
```
https://www.w3.org/WAI/demos/bad/
```
This is an intentionally bad site with many accessibility issues.

---

## Troubleshooting 🔧

### Issue: Gateway not found in ASI:One
**Solution:**
- Verify mailbox is enabled on gateway
- Check manifest is published
- Wait 2-3 minutes for indexing
- Try searching by exact agent name

### Issue: "Orchestrator missing sub-agent addresses"
**Solution:**
- Check environment variables are set correctly in Orchestrator
- Verify all 4 agent addresses are added
- Restart orchestrator agent after setting variables

### Issue: MeTTa agent fails with "File not found"
**Solution:**
- Use the inline knowledge approach (see Agent 3 alternative)
- Or upload knowledge.metta as an asset if supported

### Issue: Agents can't communicate
**Solution:**
- Verify all agents are deployed and running (green status)
- Check agent addresses are correct in environment variables
- Look at logs in Agentverse for specific error messages

---

## Address Recording Sheet 📝

Keep track of your agent addresses here:

```bash
# Copy these as you deploy each agent

# Worker Agents
ORCH_FETCHER_ADDR=agent1q
ORCH_ANALYZER_ADDR=agent1q
ORCH_METTA_ADDR=agent1q
ORCH_RESOURCES_ADDR=agent1q

# Coordination Agents
ORCHESTRATOR_ADDR=agent1q
GATEWAY_ADDR=agent1q

# For ASI:One Testing
Gateway Agent Name: a11y_gateway
Gateway Agent Address: agent1q
```



