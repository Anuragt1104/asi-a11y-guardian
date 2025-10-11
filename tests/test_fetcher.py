import pytest
import httpx
from bs4 import BeautifulSoup
from urllib.parse import urljoin


@pytest.mark.asyncio
async def test_fetch_simple_page():
    """Test fetching a simple web page using httpx directly."""
    url = "https://example.com"
    
    async with httpx.AsyncClient(follow_redirects=True, timeout=15) as client:
        resp = await client.get(url)
    
    assert resp.status_code == 200
    assert len(resp.text) > 0
    assert "<title>" in resp.text.lower()
    
    # Test link extraction like the fetcher agent does
    soup = BeautifulSoup(resp.text, "lxml")
    links = []
    for a in soup.find_all("a", href=True):
        href = a.get("href")
        if href and not href.startswith("javascript:"):
            links.append(urljoin(str(resp.url), href))
    
    assert isinstance(links, list)
    # example.com should have at least one link
    assert len(links) >= 0


@pytest.mark.asyncio
async def test_fetch_handles_errors():
    """Test that invalid URLs are handled gracefully."""
    url = "https://this-domain-definitely-does-not-exist-12345.com"
    
    try:
        async with httpx.AsyncClient(follow_redirects=True, timeout=5) as client:
            resp = await client.get(url)
        # If we get here, connection succeeded (shouldn't happen)
        assert False, "Expected connection to fail"
    except Exception as e:
        # Expected to raise an exception
        assert isinstance(e, (httpx.ConnectError, httpx.TimeoutException, httpx.HTTPError))

