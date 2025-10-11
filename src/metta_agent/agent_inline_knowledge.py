"""
MeTTa Agent with Inline Knowledge (for Agentverse deployment if file upload not supported)
This version has knowledge.metta content embedded directly in the code.
"""

import os
from pathlib import Path

from hyperon import MeTTa
from hyperon.atoms import E, S, V
from uagents import Agent, Context, Protocol

from src.common.models import MeTTaFinding, MeTTaQueryRequest, MeTTaQueryResponse


proto = Protocol(name="metta-protocol")

metta = MeTTa()

# Inline WCAG knowledge (embedded from knowledge.metta)
KNOWLEDGE = """
(Issue missing_lang)
(SC missing_lang "3.1.1" "Language of Page")
(Fix missing_lang "Add a valid lang attribute to the <html> tag, e.g., <html lang=\\"en\\">.")
(Refs missing_lang ("https://www.w3.org/WAI/WCAG21/Understanding/language-of-page/" "https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/lang"))
(Severity missing_lang high)

(Issue missing_title)
(SC missing_title "2.4.2" "Page Titled")
(Fix missing_title "Add a <title> element that concisely describes the page purpose.")
(Refs missing_title ("https://www.w3.org/WAI/WCAG21/Understanding/page-titled/" "https://developer.mozilla.org/en-US/docs/Web/HTML/Element/title"))
(Severity missing_title medium)

(Issue missing_alt)
(SC missing_alt "1.1.1" "Non-text Content")
(Fix missing_alt "Provide meaningful alt text describing the image purpose.")
(Refs missing_alt ("https://www.w3.org/WAI/WCAG21/Understanding/non-text-content/" "https://webaim.org/techniques/alttext/"))
(Severity missing_alt high)

(Issue headings_order)
(SC headings_order "2.4.6" "Headings and Labels")
(Fix headings_order "Ensure headings follow a logical outline (no jumps, start at <h1>).")
(Refs headings_order ("https://www.w3.org/WAI/WCAG21/Understanding/headings-and-labels/" "https://developer.mozilla.org/en-US/docs/Web/HTML/Element/Heading_Elements"))
(Severity headings_order medium)

(Issue missing_label)
(SC missing_label "3.3.2" "Labels or Instructions")
(Fix missing_label "Associate inputs with visible labels or aria-label/aria-labelledby.")
(Refs missing_label ("https://www.w3.org/WAI/WCAG21/Understanding/labels-or-instructions/" "https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Attributes/aria-label"))
(Severity missing_label high)

(Issue bad_link_text)
(SC bad_link_text "2.4.4" "Link Purpose (In Context)")
(Fix bad_link_text "Use descriptive link text that indicates the link destination or purpose.")
(Refs bad_link_text ("https://www.w3.org/WAI/WCAG21/Understanding/link-purpose-in-context/" "https://www.w3.org/WAI/tutorials/page-structure/links/"))
(Severity bad_link_text low)

; Query: map issue code -> SC, Title, Severity, Fix, Refs
(= (map-issue $code $sc $title $severity $fix $refs)
   (match &self
     (,
       (Issue $code)
       (SC $code $sc $title)
       (Severity $code $severity)
       (Fix $code $fix)
       (Refs $code $refs)
     )
     (Result $sc $title $severity $fix $refs)
   )
)
"""

# Load knowledge inline
metta.run(KNOWLEDGE)


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

