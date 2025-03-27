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
    
    logging.info(f"Performing search with query: {query}, count: {count}, offset: {offset}")
    data = await make_brave_request(url)
    
    # Check for errors first
    if "error" in data:
        logging.warning(f"Search error for query '{query}': {data['error']}")
        return f"Search error: {data['error']}"
    
    # Check for valid response structure
    if "web" not in data:
        logging.warning(f"Unexpected response format for query '{query}': 'web' key not found")
        return "Error: Unexpected response format from search API"
    
    if "results" not in data["web"] or not data["web"]["results"]:
        logging.info(f"No results found for query: '{query}'")
        return "No search results found for your query."
    
    # Process successful results
    results = data["web"]["results"]
    logging.info(f"Found {len(results)} results for query: '{query}'")
    
    formatted_results = []
    for i, result in enumerate(results, 1):
        title = result.get("title", "No title")
        url = result.get("url", "No URL")
        description = result.get("description", "No description")
        
        formatted_result = f"[Result {i}]\n"
        formatted_result += f"Title: {title}\n"
        formatted_result += f"URL: {url}\n"
        formatted_result += f"Description: {description}"
        
        formatted_results.append(formatted_result)
    
    return "\n\n".join(formatted_results)

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

async def make_brave_request(url: str) -> dict[str, Any]:
    """Helper function to make requests to the Brave API with better error handling."""
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, headers=HEADERS, timeout=10.0)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPStatusError as e:
        status_code = e.response.status_code
        logging.error(f"HTTP error {status_code} for URL {url}: {str(e)}")
        # Return structured error for different status codes
        if status_code == 401:
            return {"error": "API authentication failed - check your API key"}
        elif status_code == 429:
            return {"error": "Rate limit exceeded - try again later"}
        else:
            return {"error": f"API error: {status_code}"}
    except httpx.RequestError as e:
        logging.error(f"Request error for URL {url}: {str(e)}")
        return {"error": "Failed to connect to search API"}
    except json.JSONDecodeError as e:
        logging.error(f"Failed to decode JSON response: {str(e)}")
        return {"error": "Invalid response format"}
    except Exception as e:
        logging.error(f"Unexpected error making API request: {str(e)}")
        return {"error": "An unexpected error occurred"}

if __name__ == "__main__":
    mcp.run(transport="stdio")
