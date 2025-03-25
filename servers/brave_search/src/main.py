import json
from typing import Any
import os
from urllib.parse import urlencode
import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
import logging

# Load environment variables
load_dotenv()

BRAVE_API_KEY = os.getenv("BRAVE_API_KEY")
if not BRAVE_API_KEY:
    raise RuntimeError("Error: BRAVE_API_KEY environment variable is required")

# Initialize Logging
logging.basicConfig(level=logging.INFO)

# Initialize FastMCP server
mcp = FastMCP("brave_search")

BRAVE_API_BASE = "https://api.search.brave.com/res/v1"
HEADERS = {
    "Accept": "application/json",
    "X-Subscription-Token": BRAVE_API_KEY
}

@mcp.tool()
async def brave_web_search(query: str, count: int = 10, offset: int = 0) -> str:
    """Performs a web search using the Brave Search API."""
    params = {
        "q": query,
        "count": min(count, 20),
        "offset": offset
    }
    url = f"{BRAVE_API_BASE}/web/search?{urlencode(params)}"
    data = await make_brave_request(url)
    
    if not data or "web" not in data or "results" not in data["web"]:
        return "No search results found."
    
    results = data["web"]["results"]
    return "\n---\n".join([f"Title: {r['title']}\nDescription: {r['description']}\nURL: {r['url']}" for r in results])

@mcp.tool()
async def brave_local_search(query: str, count: int = 5) -> str:
    """Searches for local businesses using Brave's Local Search API."""
    url = f"{BRAVE_API_BASE}/web/search?q={query}&search_lang=en&result_filter=locations&count={min(count, 20)}"
    data = await make_brave_request(url)
    
    if not data or "locations" not in data or "results" not in data["locations"]:
        return "No local results found."
    
    location_ids = [r["id"] for r in data["locations"]["results"] if "id" in r]
    if not location_ids:
        return await brave_web_search(query, count)
    
    return f"Found {len(location_ids)} locations for query: {query}"

async def make_brave_request(url: str) -> Any:
    """Helper function to make requests to the Brave API."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=HEADERS, timeout=10.0)
            response.raise_for_status()  # Raise exception for 4XX/5XX status codes
            return response.json()
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error occurred: {str(e)}, Status code: {e.response.status_code}")
        return {"error": f"API error: {e.response.status_code}"}
    except httpx.RequestError as e:
        logging.error(f"Request error occurred: {str(e)}")
        return {"error": "Failed to connect to search API"}
    except json.JSONDecodeError:
        logging.error("Failed to decode JSON response")
        return {"error": "Invalid response format"}

if __name__ == "__main__":
    mcp.run(transport="stdio")
