import os
from pathlib import Path

from hyperon import MeTTa
from hyperon.atoms import E, S, V
from uagents import Agent, Context, Protocol

from src.common.models import MeTTaFinding, MeTTaQueryRequest, MeTTaQueryResponse


proto = Protocol(name="metta-protocol")

metta = MeTTa()

# Use absolute path relative to this file's location
knowledge_path = Path(__file__).parent / "knowledge.metta"
with open(knowledge_path, "r", encoding="utf-8") as f:
    metta.run(f.read())


def map_issue(issue_code: str) -> MeTTaFinding | None:
    res = metta.run(f"! (map-issue {issue_code} $sc $title $severity $fix $refs)")
    if not res or not res[0]:
        return None
    # Parse result list like: [[(Result sc title severity fix refs)]]
    # Expected: (Result "1.1.1" "Non-text Content" high "fix text" ("ref1" "ref2"))
    line = str(res[0][0])
    try:
        # Extract quoted strings: sc, title, fix, and refs
        parts = line.split('"')
        if len(parts) < 6:
            return None
        
        sc = parts[1]  # First quoted string
        title = parts[3]  # Second quoted string
        fix = parts[5]  # Third quoted string
        
        # Extract severity (unquoted token between title and fix)
        middle = parts[4]  # Text between second and third quoted string
        severity = middle.strip().split()[0] if middle.strip() else "medium"
        
        # Extract refs from the remaining parts (all quoted strings after fix)
        refs = []
        for i in range(7, len(parts), 2):
            if parts[i].strip() and parts[i] not in ('(', ')', ','):
                refs.append(parts[i])
        
        return MeTTaFinding(sc=sc, title=title, severity=severity, fix=fix, references=refs)
    except Exception as e:  # noqa: BLE001
        return None


@proto.on_message(MeTTaQueryRequest)
async def on_query(ctx: Context, sender: str, msg: MeTTaQueryRequest):
    finding = map_issue(msg.issue_code)
    if finding is None:
        ctx.logger.warning(f"No MeTTa mapping found for {msg.issue_code}")
        return
    await ctx.send(sender, MeTTaQueryResponse(issue_code=msg.issue_code, finding=finding))


agent = Agent(name="a11y_metta")
agent.include(proto)


if __name__ == "__main__":
    agent.run()
