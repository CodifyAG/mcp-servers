import json
from typing import Any
import os
from urllib.parse import urlencode, urlparse
from bs4 import BeautifulSoup
import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
import logging

from brave_search_mcp.models import WebSearchRequest

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
    """Fetches content from a website and returns cleaned text.
    
    Args:
        url: The URL of the website to fetch
        
    Returns:
        Clean text content from the website
    """
    if not is_valid_url(url):
        return "Invalid URL format"
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url, follow_redirects=True, timeout=10.0)
            response.raise_for_status()
            
            html_content = response.text
            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Remove script and style elements
            for element in soup(['script', 'style']):
                element.decompose()
                
            # Get clean text
            text = soup.get_text(separator='\n')
            
            # Clean up whitespace
            lines = (line.strip() for line in text.splitlines())
            chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
            text = '\n'.join(chunk for chunk in chunks if chunk)
            
            # Truncate if too long
            if len(text) > 10000:
                text = text[:10000] + "...\n[Content truncated due to length]"
                
            return text
    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error {e.response.status_code} for URL {url}: {str(e)}")
        return f"Error fetching website: HTTP {e.response.status_code}"
    except httpx.RequestError as e:
        logging.error(f"Request error for URL {url}: {str(e)}")
        return f"Error connecting to website: {str(e)}"
    except Exception as e:
        logging.error(f"Unexpected error fetching website: {str(e)}")
        return f"Error processing website content: {str(e)}"

async def make_brave_request(url: str) -> dict[str, Any]:
    """Helper function to make requests to the Brave API with better error handling."""
    try:
        async with httpx.AsyncClient() as client:
            logging.info(f"Making request to Brave API: {url}")
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

def is_valid_url(url: str) -> bool:
    """Check if the URL is valid and uses http or https."""
    try:
        result = urlparse(url)
        return all([result.scheme in ['http', 'https'], result.netloc])
    except ValueError:
        return False

def main():
    """Main function to run the MCP server."""
    # This function is not strictly necessary, as the server is started in the if __name__ block
    mcp.run(transport="stdio")
    
