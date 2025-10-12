"""
Orchestrator Agent - Agentverse Ready (Standalone)
Copy this entire file into Agentverse "Blank Agent"
"""

import os
from collections import Counter
from typing import List, Optional, Dict
from urllib.parse import urlparse
from uagents import Agent, Context, Protocol, Model


# Models (inline - no external imports needed)
class AuditRequest(Model):
    url: str
    depth: Optional[int] = 1


class FetchContentRequest(Model):
    url: str


class FetchContentResponse(Model):
    url: str
    status_code: int
    final_url: str
    html: str
    links: List[str]


class AnalysisRequest(Model):
    url: str
    html: str


class Issue(Model):
    code: str  # e.g., "missing_alt", "headings_order", "missing_label", "missing_lang", "missing_title", "bad_link_text"
    message: str
    location: Optional[str] = None  # e.g., a tag summary or CSS-like hint
    snippet: Optional[str] = None


class AnalysisResponse(Model):
    url: str
    issues: List[Issue]
    warnings: Optional[List[str]] = None


class MeTTaFinding(Model):
    sc: str  # WCAG Success Criterion code (e.g., "1.1.1")
    title: str
    severity: str  # low | medium | high | critical
    fix: str
    references: List[str]


class MeTTaQueryRequest(Model):
    issue_code: str


class MeTTaQueryResponse(Model):
    issue_code: str
    finding: MeTTaFinding


class ResourceRequest(Model):
    issue_code: str


class ResourceResponse(Model):
    issue_code: str
    links: List[str]


class OrchestratorReportItem(Model):
    issue: Issue
    mapping: MeTTaFinding
    resources: List[str]


class AuditReport(Model):
    url: str
    item_count: int
    by_severity: Dict[str, int]
    items: List[OrchestratorReportItem]
    summary: str


# Settings (inline - no external imports needed)
class Settings:
    def __init__(self):
        self.agentverse_token: str = os.getenv("AGENTVERSE_TOKEN", "")
        self.mailbox_secret: str = os.getenv("MAILBOX_SECRET", "")
        self.asi_one_api_key: str = os.getenv("ASI_ONE_API_KEY", "")
        self.openai_api_key: str = os.getenv("OPENAI_API_KEY", "")
        self.claude_api_key: str = os.getenv("CLAUDE_API_KEY", "")
        self.orchestrator_addr: str = os.getenv("ORCHESTRATOR_ADDR", "")
        self.orch_fetcher_addr: str = os.getenv("ORCH_FETCHER_ADDR", "")
        self.orch_analyzer_addr: str = os.getenv("ORCH_ANALYZER_ADDR", "")
        self.orch_metta_addr: str = os.getenv("ORCH_METTA_ADDR", "")
        self.orch_resources_addr: str = os.getenv("ORCH_RESOURCES_ADDR", "")


settings = Settings()


# Protocol
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
    # load from env if available
    if settings.orch_fetcher_addr:
        addresses.fetcher = settings.orch_fetcher_addr
    if settings.orch_analyzer_addr:
        addresses.analyzer = settings.orch_analyzer_addr
    if settings.orch_metta_addr:
        addresses.metta = settings.orch_metta_addr
    if settings.orch_resources_addr:
        addresses.resources = settings.orch_resources_addr

    if not (addresses.fetcher and addresses.analyzer and addresses.metta and addresses.resources):
        ctx.logger.error("Orchestrator missing sub-agent addresses. Configure before use.")
        return

    # Helper to audit a single URL
    async def audit_single(url: str):
        fetch_resp, ok = await ctx.send_and_receive(addresses.fetcher, FetchContentRequest(url=url), FetchContentResponse)
        if not ok or fetch_resp.status_code == 0:
            return None, None
        analysis_resp, ok = await ctx.send_and_receive(
            addresses.analyzer,
            AnalysisRequest(url=url, html=fetch_resp.html),
            AnalysisResponse,
        )
        if not ok:
            return None, None
        return fetch_resp, analysis_resp

    # 1) Fetch + analyze seed URL
    fetch_resp, analysis_resp = await audit_single(msg.url)
    if fetch_resp is None or analysis_resp is None:
        ctx.logger.error(f"Failed to audit {msg.url}")
        return

    # 2) Depth-limited crawl (same host only)
    to_visit = []
    visited = set([msg.url])
    depth = max(1, (msg.depth or 1))
    # seed links limited
    for l in fetch_resp.links[:20]:
        to_visit.append((l, 2))

    all_issues = {msg.url: analysis_resp.issues}

    while to_visit:
        link, d = to_visit.pop(0)
        if d > depth:
            continue
        if link in visited:
            continue
        # same host filter
        try:
            if urlparse(link).netloc != urlparse(msg.url).netloc:
                continue
        except Exception:
            continue
        visited.add(link)
        fr, ar = await audit_single(link)
        if fr is None or ar is None:
            continue
        all_issues[link] = ar.issues
        for l2 in fr.links[:10]:
            to_visit.append((l2, d + 1))

    # 3) MeTTa mapping + resources in parallel for all pages
    for page, issues in all_issues.items():
        for issue in issues:
            await ctx.send(addresses.metta, MeTTaQueryRequest(issue_code=issue.code))
            await ctx.send(addresses.resources, ResourceRequest(issue_code=issue.code))

    await ctx.sleep(0.5)
    mappings: dict[str, MeTTaFinding] = ctx.storage.get("metta_mappings") or {}
    reslinks: dict[str, list[str]] = ctx.storage.get("resource_links") or {}

    items: list[OrchestratorReportItem] = []
    severities = []
    for page, issues in all_issues.items():
        for issue in issues:
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
    summary = f"Audited up to depth {depth}. Total issues: {len(items)}. Severity breakdown: {by_sev}"
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
