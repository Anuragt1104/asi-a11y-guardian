# Local Testing Guide

This guide walks you through testing the A11y Guardian multi-agent system locally before deploying to Agentverse.

## Prerequisites

- Python 3.11
- Virtual environment set up (via `./scripts/bootstrap.sh`)

## Step 1: Run Unit Tests

First, verify that all individual agents work correctly:

```bash
# Activate virtual environment
source .venv/bin/activate

# Run all tests
PYTHONPATH=/Users/anuragtiwari/asi-a11y-guardian pytest tests/ -v
```

Expected results:
- ✅ `test_analyzer.py` - Tests HTML accessibility analysis
- ✅ `test_metta.py` - Tests WCAG knowledge graph mapping
- ✅ `test_fetcher.py` - Tests HTTP fetching and link extraction

## Step 2: Manual Agent Testing

### 2.1 Start All Agents

Open 6 separate terminal windows and run each agent:

**Terminal 1 - Fetcher Agent:**
```bash
cd /Users/anuragtiwari/asi-a11y-guardian
source .venv/bin/activate
python -m src.fetcher_agent.agent
```

**Terminal 2 - Analyzer Agent:**
```bash
cd /Users/anuragtiwari/asi-a11y-guardian
source .venv/bin/activate
python -m src.analyzer_agent.agent
```

**Terminal 3 - MeTTa Agent:**
```bash
cd /Users/anuragtiwari/asi-a11y-guardian
source .venv/bin/activate
python -m src.metta_agent.agent
```

**Terminal 4 - Resource Agent:**
```bash
cd /Users/anuragtiwari/asi-a11y-guardian
source .venv/bin/activate
python -m src.resource_agent.agent
```

**Terminal 5 - Orchestrator Agent:**
```bash
cd /Users/anuragtiwari/asi-a11y-guardian
source .venv/bin/activate
python -m src.orchestrator_agent.agent
```

**Terminal 6 - Gateway Agent:**
```bash
cd /Users/anuragtiwari/asi-a11y-guardian
source .venv/bin/activate
python -m src.gateway_agent.agent
```

### 2.2 Capture Agent Addresses

After each agent starts, you'll see output like:

```
Agent address: agent1q2kxet3vh0scsf0sm7y2eeyt94...
```

Copy these addresses and update your `.env` file:

```bash
# Edit .env or create it from env.template
cp env.template .env

# Then add the addresses:
ORCHESTRATOR_ADDR=agent1q...  # From orchestrator terminal
ORCH_FETCHER_ADDR=agent1q...  # From fetcher terminal
ORCH_ANALYZER_ADDR=agent1q... # From analyzer terminal
ORCH_METTA_ADDR=agent1q...    # From metta terminal
ORCH_RESOURCES_ADDR=agent1q... # From resource terminal
```

### 2.3 Restart Orchestrator and Gateway

After updating `.env`, restart the orchestrator and gateway agents so they pick up the new addresses.

## Step 3: Test Accessibility Audit

### Option A: Using Python Script

Create a test script `test_local_audit.py`:

```python
import asyncio
from uagents import Agent, Context
from src.common.models import AuditRequest

async def test_audit():
    # Create a test agent to send audit request
    test_agent = Agent(name="test_client")
    
    @test_agent.on_event("startup")
    async def send_audit(ctx: Context):
        # Replace with your gateway address
        gateway_addr = "agent1q..."  
        
        # Send audit request
        audit_req = AuditRequest(url="https://example.com", depth=1)
        await ctx.send(gateway_addr, audit_req)
        ctx.logger.info("Audit request sent!")
        
        # Wait a bit for response
        await asyncio.sleep(5)
    
    test_agent.run()

if __name__ == "__main__":
    asyncio.run(test_audit())
```

Run it:
```bash
python test_local_audit.py
```

### Option B: Monitor Agent Logs

Watch the terminal outputs to see the agent collaboration:

1. **Gateway** receives the audit request
2. **Orchestrator** coordinates the workflow
3. **Fetcher** downloads the HTML
4. **Analyzer** extracts accessibility issues
5. **MeTTa** maps issues to WCAG Success Criteria
6. **Resource** provides W3C/MDN reference links
7. **Orchestrator** aggregates and sends report back
8. **Gateway** displays the final report

## Step 4: Verify Output

Expected output from Gateway terminal:

```
Audit Summary for https://example.com
Issues: 3
By severity: {'high': 2, 'medium': 1}

1. [high] missing_lang - <html> element is missing a lang attribute.
   Fix: Add a valid lang attribute to the <html> tag, e.g., <html lang="en">.
   Refs: https://www.w3.org/WAI/WCAG21/Understanding/language-of-page/

2. [high] missing_alt - Image is missing meaningful alt text.
   Fix: Provide meaningful alt text describing the image purpose.
   Refs: https://www.w3.org/WAI/WCAG21/Understanding/non-text-content/

3. [medium] missing_title - Document is missing a <title> element.
   Fix: Add a <title> element that concisely describes the page purpose.
   Refs: https://www.w3.org/WAI/WCAG21/Understanding/page-titled/
```

## Step 5: Test Different URLs

Try these test cases:

### Easy Test - Example.com
```python
AuditRequest(url="https://example.com", depth=1)
```
Expected: Few issues, simple structure

### Moderate Test - W3C Bad Example
```python
AuditRequest(url="https://www.w3.org/WAI/demos/bad/", depth=1)
```
Expected: Many accessibility issues (intentionally bad site)

### Complex Test - Multi-page Crawl
```python
AuditRequest(url="https://example.com", depth=2)
```
Expected: Issues aggregated from multiple pages

## Troubleshooting

### Issue: Agents can't connect
**Solution:** Make sure all agents are running and addresses in `.env` are correct

### Issue: "Orchestrator missing sub-agent addresses"
**Solution:** Update `.env` with all agent addresses and restart orchestrator

### Issue: MeTTa mapping returns None
**Solution:** Check that `src/metta_agent/knowledge.metta` is present and readable

### Issue: Fetcher times out
**Solution:** Check internet connection, try a different URL

## Next Steps

Once local testing works, proceed to [DEPLOYMENT.md](./DEPLOYMENT.md) for Agentverse deployment instructions.

