"""
Fetcher Agent - Agentverse Ready (Standalone)
Copy this entire file into Agentverse "Blank Agent"
"""

from urllib.parse import urljoin
from typing import List

import httpx
from bs4 import BeautifulSoup
from uagents import Agent, Context, Protocol, Model


# Models (inline - no external imports needed)
class FetchContentRequest(Model):
    url: str


class FetchContentResponse(Model):
    url: str
    status_code: int
    final_url: str
    html: str
    links: List[str]


# Protocol
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
                links.append(urljoin(str(resp.url), href))
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

