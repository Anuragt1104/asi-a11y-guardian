# Agentverse Setup Help - Code Upload Method

## ⚠️ Important: Use "Blank Agent" or "Code Editor" Option

When creating your agent in Agentverse, you have different options:

### ✅ CORRECT METHOD: Direct Code Upload

1. Click **"Create Agent"** or **"New Agent"**
2. Choose one of these options:
   - **"Blank Agent"** - Empty template you paste code into
   - **"Code Editor"** - Direct code editing
   - **"Python Agent"** - Basic Python agent template
   
3. **DO NOT** choose:
   - ❌ "Deploy from URL"
   - ❌ "GitHub Integration" 
   - ❌ "Endpoint/Webhook" options

### If Agentverse Asks for URL/Endpoint:

**Skip it or leave it blank!** 

Our agents run **inside Agentverse** - they don't need external URLs.

---

## Step-by-Step: Creating Agent 1 (Fetcher)

### Step 1: Go to Agentverse
https://agentverse.ai/agents

### Step 2: Create New Agent
Click **"+ Create Agent"** or **"New Agent"**

### Step 3: Choose Creation Method
Select **"Blank Agent"** or **"Code Editor"**

### Step 4: Basic Info
- **Name:** `a11y_fetcher`
- **Description:** (optional) "Fetches and parses web pages for accessibility auditing"
- **URL/Endpoint:** Leave blank or skip this field!

### Step 5: Paste Code
In the code editor section, paste this entire code:

```python
import re
from urllib.parse import urljoin

import httpx
from bs4 import BeautifulSoup
from uagents import Agent, Context, Protocol

from src.common.models import FetchContentRequest, FetchContentResponse


proto = Protocol(name="fetcher-protocol")


@proto.on_message(FetchContentRequest)
async def on_fetch(ctx: Context, sender: str, msg: FetchContentRequest):
    url = msg.url
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=15) as client:
            resp = await client.get(url)
        html = resp.text or ""
        soup = BeautifulSoup(html, "lxml")
        links = []
        for a in soup.find_all("a", href=True):
            href = a.get("href")
            if href and not href.startswith("javascript:"):
                links.append(urljoin(resp.url.__str__(), href))
        await ctx.send(
            sender,
            FetchContentResponse(
                url=url,
                status_code=resp.status_code,
                final_url=str(resp.url),
                html=html,
                links=list(dict.fromkeys(links)),
            ),
        )
    except Exception as e:  # noqa: BLE001
        await ctx.send(
            sender,
            FetchContentResponse(
                url=url,
                status_code=0,
                final_url=url,
                html="",
                links=[],
            ),
        )
        ctx.logger.error(f"Fetcher error for {url}: {e}")


agent = Agent(name="a11y_fetcher")
agent.include(proto)


if __name__ == "__main__":
    agent.run()
```

### Step 6: Add Dependencies/Requirements
Look for **"Dependencies"** or **"Requirements"** section and add:

```
uagents>=0.15,<0.17
uagents-core==0.3.10
httpx==0.27.2
beautifulsoup4==4.12.3
lxml==5.3.0
```

### Step 7: Handle Missing Models Import

⚠️ **Important:** The code imports `from src.common.models import ...`

Agentverse might not have access to your `src/common/models.py` file. You have 2 options:

**Option A: Include models.py as additional file**
- Some Agentverse versions let you upload multiple files
- Upload `src/common/models.py` as an additional file

**Option B: Inline the models (simpler)**
- See below for agent code with inline models

### Step 8: Save and Deploy
- Click **"Save"** or **"Deploy"**
- Wait for agent to start (shows green/running status)
- **Copy the agent address** (format: `agent1q...`)

---

## 🔧 Alternative: Agent with Inline Models

If Agentverse can't find `src.common.models`, use this version instead:

```python
import re
from urllib.parse import urljoin
from typing import List

import httpx
from bs4 import BeautifulSoup
from uagents import Agent, Context, Protocol, Model


# Inline models
class FetchContentRequest(Model):
    url: str


class FetchContentResponse(Model):
    url: str
    status_code: int
    final_url: str
    html: str
    links: List[str]


# Agent code
proto = Protocol(name="fetcher-protocol")


@proto.on_message(FetchContentRequest)
async def on_fetch(ctx: Context, sender: str, msg: FetchContentRequest):
    url = msg.url
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=15) as client:
            resp = await client.get(url)
        html = resp.text or ""
        soup = BeautifulSoup(html, "lxml")
        links = []
        for a in soup.find_all("a", href=True):
            href = a.get("href")
            if href and not href.startswith("javascript:"):
                links.append(urljoin(resp.url.__str__(), href))
        await ctx.send(
            sender,
            FetchContentResponse(
                url=url,
                status_code=resp.status_code,
                final_url=str(resp.url),
                html=html,
                links=list(dict.fromkeys(links)),
            ),
        )
    except Exception as e:
        await ctx.send(
            sender,
            FetchContentResponse(
                url=url,
                status_code=0,
                final_url=url,
                html="",
                links=[],
            ),
        )
        ctx.logger.error(f"Fetcher error for {url}: {e}")


agent = Agent(name="a11y_fetcher")
agent.include(proto)


if __name__ == "__main__":
    agent.run()
```

---

## 📸 What the Agentverse UI Should Look Like:

You should see sections like:
- [ ] **Agent Name:** Enter `a11y_fetcher`
- [ ] **Code Editor:** Big text box - paste the code here
- [ ] **Requirements/Dependencies:** List of packages
- [ ] **Environment Variables:** (skip for fetcher agent)
- [ ] **Save/Deploy Button:** Click when ready

---

## ❓ Still Stuck?

**If you see these fields, here's what to do:**

- **"Agent URL"** → Leave blank or enter: `http://localhost:8000`
- **"Webhook URL"** → Leave blank
- **"Endpoint"** → Leave blank  
- **"Host"** → Leave default or blank
- **"Port"** → Leave default (8000) or blank

**These fields are for external agents, not for code uploaded directly!**

---

## ✅ Quick Checklist

Before clicking Deploy:
- [ ] Agent name is set: `a11y_fetcher`
- [ ] Code is pasted in editor
- [ ] 5 requirements/dependencies added
- [ ] No errors showing in code editor
- [ ] Ready to deploy!

---

Next: Come back and tell me if agent deployed successfully or if you're still stuck!
