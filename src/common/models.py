from typing import List, Optional

from uagents import Model


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


class MeTTaQueryRequest(Model):
    issue_code: str


class MeTTaFinding(Model):
    sc: str  # WCAG Success Criterion code (e.g., "1.1.1")
    title: str
    severity: str  # low | medium | high | critical
    fix: str
    references: List[str]


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
    by_severity: dict
    items: List[OrchestratorReportItem]
    summary: str
