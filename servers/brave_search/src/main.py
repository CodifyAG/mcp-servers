import json
from typing import Any
import os
from urllib.parse import urlencode
from bs4 import BeautifulSoup
import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
import logging

from models import WebSearchRequest

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
    request = WebSearchRequest(q=query, count=count, offset=offset)
    params = request.model_dump()
    url = f"{BRAVE_API_BASE}/web/search?{urlencode(params)}"
    data = await make_brave_request(url)
    
    if not data or "web" not in data or "results" not in data["web"]:
        return "No search results found."
    
    results = data["web"]["results"]
    return "\n---\n".join([f"Title: {r['title']}\nDescription: {r['description']}\nURL: {r['url']}" for r in results])

@mcp.tool()
async def fetch_website(url: str) -> str:
    async with httpx.AsyncClient() as client:
        response = await client.get(url)
        if response.status_code != 200:
            print(f"Failed to fetch page. Status code: {response.status_code}")
            return None
    
    soup = BeautifulSoup(response, 'html.parser')
    for s in soup(['script', 'style']):
        s.decompose()
    text = soup.get_text() 
    lines = (line.strip() for line in text.splitlines())
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    text = '\n'.join(chunk for chunk in chunks if chunk)
    return text



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
