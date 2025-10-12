"""
Gateway Agent - Agentverse Ready (Standalone)
Copy this entire file into Agentverse "Blank Agent"
"""

import os
from datetime import datetime
from typing import Dict, List, Optional, Any
from uuid import uuid4
import httpx
import asyncio
from uagents import Agent, Context, Protocol, Model


# Models (inline - no external imports needed)
class AuditReport(Model):
    url: str
    item_count: int
    by_severity: Dict[str, int]
    items: List[Any]  # OrchestratorReportItem
    summary: str


class AuditRequest(Model):
    url: str
    depth: Optional[int] = 1


# Chat Protocol Components (inline)
class ChatAcknowledgement(Model):
    timestamp: datetime
    acknowledged_msg_id: str


class TextContent(Model):
    type: str = "text"
    text: str


class StartSessionContent(Model):
    type: str = "start_session"


class EndSessionContent(Model):
    type: str = "end_session"


class ChatMessage(Model):
    timestamp: datetime
    msg_id: str
    content: List[Any]  # List of content items


# Agent setup
agent = Agent(name="a11y_gateway", mailbox=True)

chat_proto = Protocol(name="chat", version="1.0")
orchestrator_proto = Protocol(name="gateway-orchestrator")


def create_text_chat(text: str) -> ChatMessage:
    content = [TextContent(type="text", text=text)]
    return ChatMessage(timestamp=datetime.utcnow(), msg_id=uuid4(), content=content)


ORCHESTRATOR_ADDR_KEY = "orchestrator_addr"
ASI_ONE_API_KEY = "asi_one_api_key"
ASI_ONE_BASE_URL = "https://api.asi.one"


class ASIOneClient:
    """ASI:One API client for sending messages"""

    def __init__(self, api_key: str, base_url: str = ASI_ONE_BASE_URL):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    async def send_message(self, agent_address: str, message: str) -> Optional[str]:
        """Send a message to an agent via ASI:One"""
        try:
            async with httpx.AsyncClient(timeout=30) as client:
                response = await client.post(
                    f"{self.base_url}/chat",
                    json={
                        "agent_address": agent_address,
                        "message": message
                    },
                    headers=self.headers
                )
                response.raise_for_status()
                return response.json().get("response")
        except Exception as e:
            print(f"ASI:One API error: {e}")
            return None


@chat_proto.on_message(ChatMessage)
async def handle_message(ctx: Context, sender: str, msg: ChatMessage):
    await ctx.send(sender, ChatAcknowledgement(timestamp=datetime.utcnow(), acknowledged_msg_id=msg.msg_id))

    for item in msg.content:
        if isinstance(item, StartSessionContent):
            ctx.logger.info(f"Session started with {sender}")
        elif isinstance(item, TextContent):
            text = item.text.strip()
            # Parse a URL from input text (very simple heuristic)
            url = text.split()[0]
            ctx.storage.set("last_chat_sender", sender)
            orch_addr = ctx.storage.get(ORCHESTRATOR_ADDR_KEY)
            if not orch_addr:
                await ctx.send(sender, create_text_chat("Orchestrator address not set. Use admin set command."))
                return

            # Use ASI:One if available, otherwise direct communication
            if asi_one_client:
                # Send via ASI:One API
                response = await asi_one_client.send_message(orch_addr, url)
                if response:
                    await ctx.send(sender, create_text_chat(f"ASI:One Audit Result: {response}"))
                else:
                    await ctx.send(sender, create_text_chat("Failed to get response from ASI:One API"))
            else:
                # Fallback to direct agent communication
                await ctx.send(orch_addr, AuditRequest(url=url))
                await ctx.send(sender, create_text_chat(f"Running accessibility audit for: {url}"))
        elif isinstance(item, EndSessionContent):
            ctx.logger.info(f"Session ended with {sender}")
        else:
            ctx.logger.info("Unexpected content type")


@chat_proto.on_message(ChatAcknowledgement)
async def handle_ack(ctx: Context, sender: str, msg: ChatAcknowledgement):
    ctx.logger.info(f"Ack from {sender} for {msg.acknowledged_msg_id}")


@orchestrator_proto.on_message(AuditReport)
async def on_report(ctx: Context, sender: str, msg: AuditReport):
    # Relay back to the last chat sender if stored, otherwise log
    last_sender = ctx.storage.get("last_chat_sender")
    text_lines = [
        f"Audit Summary for {msg.url}",
        f"Issues: {msg.item_count}",
        f"By severity: {msg.by_severity}",
        "",
    ]
    for i, item in enumerate(msg.items[:10], start=1):
        text_lines.append(f"{i}. [{item.mapping.severity}] {item.issue.code} - {item.issue.message}")
        text_lines.append(f"   Fix: {item.mapping.fix}")
        if item.resources:
            text_lines.append(f"   Refs: {', '.join(item.resources[:2])}")
    text = "\n".join(text_lines)
    if last_sender:
        await ctx.send(last_sender, create_text_chat(text))
    else:
        ctx.logger.info(text)


# Initialize ASI:One client if API key is available
asi_one_client = None
@agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info("Gateway agent starting up...")
    api_key = ctx.storage.get(ASI_ONE_API_KEY) or os.getenv("ASI_ONE_API_KEY")
    if api_key:
        global asi_one_client
        asi_one_client = ASIOneClient(api_key)
        ctx.logger.info("ASI:One integration enabled")
    else:
        ctx.logger.info("ASI:One integration disabled - no API key found")


agent.include(chat_proto, publish_manifest=True)
agent.include(orchestrator_proto)


if __name__ == "__main__":
    agent.run()
