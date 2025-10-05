from datetime import datetime
from uuid import uuid4

from uagents import Agent, Context, Protocol
from uagents_core.contrib.protocols.chat import (
    ChatAcknowledgement,
    ChatMessage,
    EndSessionContent,
    StartSessionContent,
    TextContent,
    chat_protocol_spec,
)

from src.common.models import AuditReport, AuditRequest


agent = Agent(name="a11y_gateway", mailbox=True)

chat_proto = Protocol(spec=chat_protocol_spec)
orchestrator_proto = Protocol(name="gateway-orchestrator")


def create_text_chat(text: str) -> ChatMessage:
    content = [TextContent(type="text", text=text)]
    return ChatMessage(timestamp=datetime.utcnow(), msg_id=uuid4(), content=content)


ORCHESTRATOR_ADDR_KEY = "orchestrator_addr"


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
            orch_addr = ctx.storage.get(ORCHESTRATOR_ADDR_KEY)
            if not orch_addr:
                await ctx.send(sender, create_text_chat("Orchestrator address not set. Use admin set command."))
                return
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


agent.include(chat_proto, publish_manifest=True)
agent.include(orchestrator_proto)


if __name__ == "__main__":
    agent.run()
