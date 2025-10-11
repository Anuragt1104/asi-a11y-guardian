# Quick Start Guide - A11y Guardian

Get the A11y Guardian multi-agent accessibility auditor running in under 5 minutes.

## Prerequisites
- Python 3.11
- Internet connection

## 1. Install Dependencies (30 seconds)
```bash
cd /Users/anuragtiwari/asi-a11y-guardian
./scripts/bootstrap.sh
```

## 2. Run Tests (10 seconds)
```bash
source .venv/bin/activate
PYTHONPATH=$PWD pytest tests/ -v
```

Expected: ✅ 4 passed

## 3. Local Multi-Agent Test (5 minutes)

### Start Agents
```bash
./scripts/run_all_agents.sh
```

### Extract Addresses
Wait 5 seconds, then:
```bash
./scripts/extract_addresses.sh
```

### Update Environment
Copy the addresses to `.env`:
```bash
# Create .env if it doesn't exist
cp env.template .env

# Edit and paste the addresses from previous step
nano .env
```

### Restart Main Agents
```bash
./scripts/restart_main_agents.sh
```

### Verify
Check logs to see agents communicating:
```bash
tail -f logs/*.log
```

You should see:
- Agents initializing
- Addresses being printed
- Orchestrator loading sub-agent addresses

### Stop Agents
```bash
./scripts/stop_all_agents.sh
```

## 4. Deploy to Agentverse

See [DEPLOYMENT.md](./DEPLOYMENT.md) for complete instructions.

Quick checklist:
1. Get Agentverse token: https://agentverse.ai
2. Deploy all 6 agents (gateway, orchestrator, fetcher, analyzer, metta, resource)
3. Configure agent addresses in environment variables
4. Enable mailbox on gateway
5. Test via ASI:One

## Need Help?

- **Local Testing Issues:** See [LOCAL_TESTING.md](./LOCAL_TESTING.md)
- **Deployment Issues:** See [DEPLOYMENT.md](./DEPLOYMENT.md)
- **Test Summary:** See [TESTING_SUMMARY.md](./TESTING_SUMMARY.md)

## What the System Does

1. **Gateway** receives URL via ASI:One chat
2. **Orchestrator** coordinates the workflow
3. **Fetcher** downloads HTML
4. **Analyzer** finds accessibility issues
5. **MeTTa** maps issues to WCAG Success Criteria
6. **Resource** provides fix references
7. **Gateway** returns comprehensive report

## Example Output

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

## Technologies

- **uAgents** (Fetch.ai) - Multi-agent framework
- **MeTTa** (SingularityNET) - Knowledge graph reasoning
- **Chat Protocol** - ASI:One integration

---

**Ready to go!** 🚀

