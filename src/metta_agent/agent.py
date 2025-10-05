from hyperon import MeTTa
from hyperon.atoms import E, S, V
from uagents import Agent, Context, Protocol

from src.common.models import MeTTaFinding, MeTTaQueryRequest, MeTTaQueryResponse


proto = Protocol(name="metta-protocol")

metta = MeTTa()

with open("src/metta_agent/knowledge.metta", "r", encoding="utf-8") as f:
    metta.run(f.read())


def map_issue(issue_code: str) -> MeTTaFinding | None:
    res = metta.run(f"! (map-issue {issue_code} $sc $title $severity $fix $refs)")
    if not res:
        return None
    # Parse result list like: (Result sc title severity fix (ref1 ref2 ...))
    # Simplistic parser over string repr
    line = str(res[0])
    # Expected: (Result 1.1.1 "Non-text Content" high "fix text" ("ref1" "ref2"))
    try:
        # naive extraction
        # split by quotes for title/fix/refs
        parts = line.split('"')
        title = parts[1]
        fix = parts[3]
        # refs block is after fix; collect quoted strings beyond index 3
        refs = []
        for i in range(5, len(parts), 2):
            if parts[i].strip():
                refs.append(parts[i])
        # extract sc and severity from non-quoted segments
        nonq = line.replace(f'"{title}"', "").replace(f'"{fix}"', "")
        sc = nonq.split()[1]
        severity = nonq.split()[3]
        return MeTTaFinding(sc=sc, title=title, severity=severity, fix=fix, references=refs)
    except Exception:  # noqa: BLE001
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
