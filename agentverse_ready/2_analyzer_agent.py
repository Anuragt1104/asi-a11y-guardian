"""
Analyzer Agent - Agentverse Ready (Standalone)
Copy this entire file into Agentverse "Blank Agent"
"""

from typing import List, Optional
from bs4 import BeautifulSoup
from uagents import Agent, Context, Protocol, Model


# Models (inline - no external imports needed)
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


# Protocol
proto = Protocol(name="analyzer-protocol")


def extract_issues(url: str, html: str) -> List[Issue]:
    issues: List[Issue] = []
    soup = BeautifulSoup(html or "", "lxml")

    # 1) Missing lang attribute on <html>
    html_tag = soup.find("html")
    if html_tag is not None:
        if not html_tag.get("lang"):
            issues.append(
                Issue(
                    code="missing_lang",
                    message="<html> element is missing a lang attribute.",
                    location="html",
                )
            )
    else:
        issues.append(Issue(code="missing_html", message="Missing <html> root element."))

    # 2) Missing <title>
    if not soup.find("title"):
        issues.append(Issue(code="missing_title", message="Document is missing a <title> element."))

    # 3) Images with missing or empty alt
    for img in soup.find_all("img"):
        alt = img.get("alt")
        if alt is None or alt.strip() == "":
            issues.append(
                Issue(
                    code="missing_alt",
                    message="Image is missing meaningful alt text.",
                    location=str(img)[:120],
                    snippet=str(img)[:240],
                )
            )

    # 4) Headings order (check simple h1->h6 monotonic increase)
    heading_levels = []
    for h in soup.find_all([f"h{i}" for i in range(1, 7)]):
        try:
            level = int(h.name[1])
            heading_levels.append(level)
        except Exception:  # noqa: BLE001
            continue
    # simple heuristic: if a step increases by >1 or starts > h1
    if heading_levels:
        if heading_levels[0] > 1:
            issues.append(
                Issue(
                    code="headings_order",
                    message="Headings should start from <h1> and follow a logical order.",
                )
            )
        for prev, curr in zip(heading_levels, heading_levels[1:]):
            if curr - prev > 1:
                issues.append(
                    Issue(
                        code="headings_order",
                        message=f"Heading jumps from h{prev} to h{curr}.",
                    )
                )
                break

    # 5) Inputs missing labels
    for input_el in soup.find_all("input"):
        id_attr = input_el.get("id")
        has_label = False
        if id_attr and soup.find("label", attrs={"for": id_attr}):
            has_label = True
        if input_el.get("aria-label") or input_el.get("aria-labelledby"):
            has_label = True
        if not has_label and input_el.get("type") not in {"hidden", "submit", "button"}:
            issues.append(
                Issue(
                    code="missing_label",
                    message="Form control input lacks an associated label.",
                    location=str(input_el)[:120],
                    snippet=str(input_el)[:240],
                )
            )

    # 6) Anchor link text generic (e.g., "click here", "read more")
    generic_texts = {"click here", "read more", "more", "here"}
    for a in soup.find_all("a"):
        text = (a.get_text() or "").strip().lower()
        if text in generic_texts:
            issues.append(
                Issue(
                    code="bad_link_text",
                    message=f"Anchor uses non-descriptive link text: '{text}'.",
                    location=str(a)[:120],
                    snippet=str(a)[:240],
                )
            )

    return issues


@proto.on_message(AnalysisRequest)
async def on_analyze(ctx: Context, sender: str, msg: AnalysisRequest):
    issues = extract_issues(msg.url, msg.html)
    await ctx.send(sender, AnalysisResponse(url=msg.url, issues=issues))


agent = Agent(name="a11y_analyzer")
agent.include(proto)


if __name__ == "__main__":
    agent.run()
