import pytest
import httpx
from unittest.mock import MagicMock, Mock, patch, AsyncMock
from brave_search_mcp.main import (
    brave_web_search,
    fetch_website,
    make_brave_request,
)

# Sample response data for mocking
WEB_SEARCH_RESPONSE = {
    "web": {
        "results": [
            {
                "title": "Test Result 1",
                "url": "https://example.com/1",
                "description": "This is test result 1",
            },
            {
                "title": "Test Result 2",
                "url": "https://example.com/2",
                "description": "This is test result 2",
            },
        ]
    }
}

ERROR_RESPONSE = {"error": "Test error message"}

# HTML content for website fetch testing
HTML_CONTENT = """
<!DOCTYPE html>
<html>
<head>
    <title>Test Page</title>
    <style>
        body { font-family: Arial; }
    </style>
</head>
<body>
    <h1>Test Page Heading</h1>
    <p>This is a paragraph.</p>
    <script>
        console.log("This should be removed");
    </script>
</body>
</html>
"""

EXPECTED_TEXT = "Test Page Heading\nThis is a paragraph."


@pytest.mark.asyncio
async def test_make_brave_request_success():
    mock_response = AsyncMock(spec=httpx.Response)
    mock_response.status_code = 200
    mock_response.headers = {"Content-Type": "application/json"}
    mock_response.json = MagicMock(return_value=WEB_SEARCH_RESPONSE)

    with patch("httpx.AsyncClient.get", return_value=mock_response):
        result = await make_brave_request("https://api.example.com/test")

    assert result == WEB_SEARCH_RESPONSE


@pytest.mark.asyncio
async def test_make_brave_request_http_error():
    mock_response = AsyncMock()
    mock_error = httpx.HTTPStatusError(
        "Error", request=AsyncMock(), response=AsyncMock()
    )
    mock_error.response.status_code = 401
    mock_response.raise_for_status = MagicMock(side_effect=mock_error)

    with patch("httpx.AsyncClient.get", return_value=mock_response):
        result = await make_brave_request("https://api.example.com/test")

    assert "error" in result
    assert "API authentication failed" in result["error"]


@pytest.mark.asyncio
async def test_make_brave_request_connection_error():
    with patch(
        "httpx.AsyncClient.get",
        side_effect=httpx.RequestError("Connection error", request=AsyncMock()),
    ):
        result = await make_brave_request("https://api.example.com/test")

    assert "error" in result
    assert "Failed to connect" in result["error"]


@pytest.mark.asyncio
async def test_brave_web_search_success():
    with patch(
        "brave_search_mcp.main.make_brave_request", return_value=WEB_SEARCH_RESPONSE
    ):
        result = await brave_web_search("test query")

    assert "Test Result 1" in result
    assert "Test Result 2" in result
    assert "https://example.com/1" in result
    assert "https://example.com/2" in result


@pytest.mark.asyncio
async def test_brave_web_search_error():
    with patch("brave_search_mcp.main.make_brave_request", return_value=ERROR_RESPONSE):
        result = await brave_web_search("test query")

    assert "Search error:" in result
    assert "Test error message" in result


@pytest.mark.asyncio
async def test_brave_web_search_no_results():
    with patch(
        "brave_search_mcp.main.make_brave_request",
        return_value={"web": {"results": []}},
    ):
        result = await brave_web_search("test query")

    assert "No search results found" in result


@pytest.mark.asyncio
async def test_fetch_website_success():
    mock_response = AsyncMock()
    mock_response.text = HTML_CONTENT
    mock_response.raise_for_status = AsyncMock()

    with patch("httpx.AsyncClient.get", return_value=mock_response):
        result = await fetch_website("https://example.com")

    assert "Test Page Heading" in result
    assert "This is a paragraph" in result
    assert "This should be removed" not in result


@pytest.mark.asyncio
async def test_fetch_website_invalid_url():
    result = await fetch_website("not-a-valid-url")
    assert "Invalid URL format" in result


@pytest.mark.asyncio
async def test_fetch_website_http_error():
    mock_error = httpx.HTTPStatusError(
        "Error", request=AsyncMock(), response=AsyncMock()
    )
    mock_error.response.status_code = 404

    with patch("httpx.AsyncClient.get", side_effect=mock_error):
        result = await fetch_website("https://example.com")

    assert "Error fetching website" in result
    assert "404" in result
