from collections import Counter, defaultdict

from uagents import Agent, Context, Protocol

from src.common.models import (
    AnalysisRequest,
    AnalysisResponse,
    AuditReport,
    AuditRequest,
    FetchContentRequest,
    FetchContentResponse,
    MeTTaFinding,
    MeTTaQueryRequest,
    MeTTaQueryResponse,
    OrchestratorReportItem,
    ResourceRequest,
    ResourceResponse,
)


proto = Protocol(name="orchestrator-protocol")


class AddressBook:
    fetcher: str | None = None
    analyzer: str | None = None
    metta: str | None = None
    resources: str | None = None


addresses = AddressBook()


@proto.on_message(FetchContentResponse)
async def on_fetch_resp(ctx: Context, sender: str, msg: FetchContentResponse):
    ctx.storage.set("fetch_response", msg)


@proto.on_message(AnalysisResponse)
async def on_analysis_resp(ctx: Context, sender: str, msg: AnalysisResponse):
    ctx.storage.set("analysis_response", msg)


@proto.on_message(MeTTaQueryResponse)
async def on_metta_resp(ctx: Context, sender: str, msg: MeTTaQueryResponse):
    mapping = ctx.storage.get("metta_mappings") or {}
    mapping[msg.issue_code] = msg.finding
    ctx.storage.set("metta_mappings", mapping)


@proto.on_message(ResourceResponse)
async def on_resource_resp(ctx: Context, sender: str, msg: ResourceResponse):
    reslinks = ctx.storage.get("resource_links") or {}
    reslinks[msg.issue_code] = msg.links
    ctx.storage.set("resource_links", reslinks)


@proto.on_message(AuditRequest)
async def on_audit(ctx: Context, sender: str, msg: AuditRequest):
    if not (addresses.fetcher and addresses.analyzer and addresses.metta and addresses.resources):
        ctx.logger.error("Orchestrator missing sub-agent addresses. Configure before use.")
        return

    # 1) Fetch content
    fetch_resp, ok = await ctx.send_and_receive(addresses.fetcher, FetchContentRequest(url=msg.url), FetchContentResponse)
    if not ok or fetch_resp.status_code == 0:
        ctx.logger.error(f"Failed to fetch {msg.url}")
        return

    # 2) Analyze
    analysis_resp, ok = await ctx.send_and_receive(
        addresses.analyzer,
        AnalysisRequest(url=msg.url, html=fetch_resp.html),
        AnalysisResponse,
    )
    if not ok:
        ctx.logger.error(f"Failed to analyze {msg.url}")
        return

    # 3) MeTTa mapping + resources in parallel
    for issue in analysis_resp.issues:
        await ctx.send(addresses.metta, MeTTaQueryRequest(issue_code=issue.code))
        await ctx.send(addresses.resources, ResourceRequest(issue_code=issue.code))

    await ctx.sleep(0.5)
    mappings: dict[str, MeTTaFinding] = ctx.storage.get("metta_mappings") or {}
    reslinks: dict[str, list[str]] = ctx.storage.get("resource_links") or {}

    items: list[OrchestratorReportItem] = []
    severities = []
    for issue in analysis_resp.issues:
        mapping = mappings.get(issue.code)
        if mapping:
            severities.append(mapping.severity)
            items.append(
                OrchestratorReportItem(
                    issue=issue,
                    mapping=mapping,
                    resources=reslinks.get(issue.code, []),
                )
            )
        else:
            items.append(
                OrchestratorReportItem(
                    issue=issue,
                    mapping=MeTTaFinding(sc="n/a", title="Unmapped issue", severity="low", fix="Review manually.", references=[]),
                    resources=reslinks.get(issue.code, []),
                )
            )

    by_sev = dict(Counter(severities)) if severities else {}
    summary = f"Found {len(items)} issues on {msg.url}. Severity breakdown: {by_sev}"
    report = AuditReport(url=msg.url, item_count=len(items), by_severity=by_sev, items=items, summary=summary)

    ctx.storage.set("metta_mappings", {})
    ctx.storage.set("resource_links", {})

    await ctx.send(sender, report)


agent = Agent(name="a11y_orchestrator")


@agent.on_event("startup")
async def startup(ctx: Context):
    ctx.logger.info("Orchestrator ready. Configure sub-agent addresses via ctx.storage or environment.")


agent.include(proto)


if __name__ == "__main__":
    agent.run()
