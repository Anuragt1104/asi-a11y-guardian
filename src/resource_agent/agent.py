from uagents import Agent, Context, Protocol

from src.common.models import ResourceRequest, ResourceResponse


proto = Protocol(name="resource-protocol")

REFERENCE_MAP = {
    "missing_lang": [
        "https://www.w3.org/WAI/WCAG21/Understanding/language-of-page/",
        "https://developer.mozilla.org/en-US/docs/Web/HTML/Global_attributes/lang",
    ],
    "missing_title": [
        "https://www.w3.org/WAI/WCAG21/Understanding/page-titled/",
        "https://developer.mozilla.org/en-US/docs/Web/HTML/Element/title",
    ],
    "missing_alt": [
        "https://www.w3.org/WAI/WCAG21/Understanding/non-text-content/",
        "https://webaim.org/techniques/alttext/",
    ],
    "headings_order": [
        "https://www.w3.org/WAI/WCAG21/Understanding/headings-and-labels/",
        "https://developer.mozilla.org/en-US/docs/Web/HTML/Element/Heading_Elements",
    ],
    "missing_label": [
        "https://www.w3.org/WAI/WCAG21/Understanding/labels-or-instructions/",
        "https://developer.mozilla.org/en-US/docs/Web/Accessibility/ARIA/Attributes/aria-label",
    ],
    "bad_link_text": [
        "https://www.w3.org/WAI/WCAG21/Understanding/link-purpose-in-context/",
        "https://www.w3.org/WAI/tutorials/page-structure/links/",
    ],
}


@proto.on_message(ResourceRequest)
async def on_resources(ctx: Context, sender: str, msg: ResourceRequest):
    links = REFERENCE_MAP.get(msg.issue_code, [])
    await ctx.send(sender, ResourceResponse(issue_code=msg.issue_code, links=links))


agent = Agent(name="a11y_resources")
agent.include(proto)


if __name__ == "__main__":
    agent.run()
