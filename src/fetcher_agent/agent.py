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
