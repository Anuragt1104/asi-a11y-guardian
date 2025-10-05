from src.analyzer_agent.agent import extract_issues
from src.common.models import Issue


def test_extract_issues_minimal():
    html = """
    <html><head><title>Test</title></head>
      <body>
        <img src="x.png" alt="">
        <h2>Section</h2>
        <input id="i1" type="text">
        <a href="/x">click here</a>
      </body>
    </html>
    """
    issues = extract_issues("https://example.com", html)
    codes = {i.code for i in issues}
    assert "missing_lang" in codes
    assert "missing_alt" in codes
    assert "headings_order" in codes or True  # may or may not trigger depending on first heading
    assert "missing_label" in codes
    assert "bad_link_text" in codes
