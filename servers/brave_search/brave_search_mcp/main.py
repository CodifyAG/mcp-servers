import json
from typing import Any
import os
from urllib.parse import urlencode, urlparse
from bs4 import BeautifulSoup
import httpx
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP
import logging

from brave_search_mcp.models import (
    WebSearchRequest,
)

load_dotenv()

BRAVE_API_KEY = os.getenv("BRAVE_API_KEY")
if not BRAVE_API_KEY:
    raise RuntimeError("Error: BRAVE_API_KEY environment variable is required")

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)

mcp = FastMCP("brave_search")

BRAVE_API_BASE = "https://api.search.brave.com/res/v1"
HEADERS = {"Accept": "application/json", "X-Subscription-Token": BRAVE_API_KEY}


@mcp.tool()
async def brave_web_search(query: str, count: int = 10, offset: int = 0) -> str:
    """
    Performs a web search using the Brave Search API and formats the results.

    Constructs the API request URL, calls the Brave API via `make_brave_request`,
    handles potential errors returned from the API call, and formats the
    successful search results into a human-readable string.

    Args:
        query (str): The search term or phrase to query.
        count (int, optional): The maximum number of search results to return.
                               Defaults to 10.
        offset (int, optional): The number of results to skip from the beginning.
                                Used for pagination. Defaults to 0.

    Returns:
        str: A formatted string containing the search results, with each result
             displaying its title, URL, and description. Returns specific error
             messages if the API call fails, encounters an issue, or if no
             results are found. Example error return: "Search error: Rate limit exceeded..."
             or "No search results found for your query.".
    """
    request = WebSearchRequest(q=query, count=count, offset=offset)
    params = request.model_dump(exclude_none=True)
    url = f"{BRAVE_API_BASE}/web/search?{urlencode(params)}"

    logging.info(
        f"Performing search with query: '{query}', count: {count}, offset: {offset}"
    )
    data = await make_brave_request(url)

    if "error" in data:
        logging.warning(f"Search error for query '{query}': {data['error']}")
        # Return the specific error message provided by make_brave_request
        return f"Search error: {data['error']}"

    if "web" not in data or "results" not in data.get("web", {}):
        logging.warning(
            f"Unexpected response format for query '{query}': 'web' or 'results' key missing. Response: {data}"
        )
        return "Error: Unexpected response format from search API"

    results = data["web"]["results"]

    if not results:
        logging.info(f"No results found for query: '{query}'")
        return "No search results found for your query."

    logging.info(f"Found {len(results)} results for query: '{query}'")

    formatted_results = []
    for i, result in enumerate(results, 1 + offset):
        title = result.get("title", "No title available")
        url_res = result.get("url", "No URL available")
        description = result.get("description", "No description available")

        formatted_result = f"[Result {i}]\n"
        formatted_result += f"  Title: {title}\n"
        formatted_result += f"  URL: {url_res}\n"
        formatted_result += f"  Description: {description}"

        formatted_results.append(formatted_result)

    return "\n\n".join(formatted_results)


@mcp.tool()
async def fetch_website(url: str) -> str:
    """
    Fetches the content of a given URL, cleans it, and returns the text.

    Uses httpx to make an asynchronous GET request, following redirects.
    Parses the HTML content using BeautifulSoup, removing script and style tags.
    Normalizes whitespace and returns the extracted text. If the text exceeds
    10000 characters, it's truncated. Handles common HTTP and network errors.

    Args:
        url (str): The URL of the website to fetch. Must start with http:// or https://.

    Returns:
        str: The cleaned text content of the website (potentially truncated),
             or a string indicating an error (e.g., "Invalid URL format",
             "Error fetching website: HTTP 404", "Error connecting to website: ...").
    """
    if not is_valid_url(url):
        logging.warning(f"Invalid URL format provided: {url}")
        return "Invalid URL format"
    try:
        headers = {"User-Agent": "Mozilla/5.0 (compatible; MyFetcherBot/1.0)"}
        async with httpx.AsyncClient() as client:
            logging.info(f"Attempting to fetch URL: {url}")
            response = await client.get(
                url, follow_redirects=True, timeout=15.0, headers=headers
            )
            response.raise_for_status()

            html_content = response.text
            soup = BeautifulSoup(html_content, "html.parser")

            for element in soup(
                ["script", "style", "nav", "footer", "header", "aside"]
            ):
                element.decompose()

            text = soup.get_text(separator="\n", strip=True)

            lines = [line for line in text.splitlines() if line.strip()]
            text = "\n".join(lines)

            max_length = 10000
            if len(text) > max_length:
                logging.info(
                    f"Content from {url} truncated to {max_length} characters."
                )
                text = (
                    text[:max_length]
                    + f"...\n[Content truncated due to length exceeding {max_length} characters]"
                )

            logging.info(
                f"Successfully fetched and cleaned content from {url} (Length: {len(text)})"
            )
            return text

    except httpx.HTTPStatusError as e:
        logging.error(f"HTTP error {e.response.status_code} fetching URL {url}: {e}")
        return f"Error fetching website: HTTP {e.response.status_code} {e.response.reason_phrase}"
    except httpx.TimeoutException as e:
        logging.error(f"Timeout error fetching URL {url}: {e}")
        return f"Error fetching website: Request timed out after {e.request.extensions.get('timeout', {}).get('connect')} seconds"
    except httpx.RequestError as e:
        logging.error(f"Request error fetching URL {url}: {e}")
        return f"Error connecting to website: {e.__class__.__name__}"
    except Exception as e:
        logging.error(f"Unexpected error processing website {url}: {e}", exc_info=True)
        return f"Error processing website content: {e.__class__.__name__}"


async def make_brave_request(url: str) -> dict[str, Any]:
    """
    Helper function to make GET requests to the Brave Search API.

    Handles authentication using the global BRAVE_API_KEY, sets appropriate
    headers, manages timeouts, and provides structured error handling for
    common issues like authentication failure, rate limiting, connection problems,
    and invalid responses.

    Args:
        url (str): The complete URL for the Brave API endpoint, including
                   any necessary query parameters.

    Returns:
        dict[str, Any]: A dictionary containing the parsed JSON response from the
                        Brave API on success. On failure, returns a dictionary
                        with a single 'error' key containing a descriptive
                        error message (e.g., {'error': 'API authentication failed...'}).
    """
    try:
        async with httpx.AsyncClient() as client:
            logging.debug(f"Making Brave API request to: {url}")
            response = await client.get(url, headers=HEADERS, timeout=10.0)
            response.raise_for_status()

            try:
                data = response.json()
                logging.debug(f"Received successful response from Brave API for {url}")
                return data
            except json.JSONDecodeError as e:
                logging.error(
                    f"Failed to decode JSON response from {url}. Status: {response.status_code}. Response text: {response.text[:200]}... Error: {e}"
                )
                return {"error": "Invalid JSON response received from API"}

    except httpx.HTTPStatusError as e:
        status_code = e.response.status_code
        logging.error(f"HTTP error {status_code} from Brave API URL {url}: {e}")
        if status_code == 401:
            return {"error": "API authentication failed - check your BRAVE_API_KEY"}
        elif status_code == 403:
            return {"error": "Permission denied - check API key or subscription plan"}
        elif status_code == 429:
            return {"error": "Rate limit exceeded - please wait before trying again"}
        elif status_code >= 500:
            return {
                "error": f"Brave API server error: {status_code} {e.response.reason_phrase}"
            }
        else:
            try:
                error_detail = e.response.json()
                message = error_detail.get("message", e.response.text)
            except json.JSONDecodeError:
                message = e.response.text
            logging.warning(
                f"Client error {status_code} from Brave API: {message[:200]}"
            )
            return {"error": f"API client error: {status_code} - {message[:100]}"}

    except httpx.TimeoutException as e:
        logging.error(f"Timeout error connecting to Brave API URL {url}: {e}")
        return {"error": "Request to search API timed out"}
    except httpx.RequestError as e:
        logging.error(f"Network error connecting to Brave API URL {url}: {e}")
        return {"error": f"Failed to connect to search API: {e.__class__.__name__}"}
    except Exception as e:
        logging.error(
            f"Unexpected error during Brave API request to {url}: {e}", exc_info=True
        )
        return {"error": f"An unexpected error occurred: {e.__class__.__name__}"}


def is_valid_url(url: str) -> bool:
    """
    Checks if the provided string is a valid HTTP or HTTPS URL.

    Uses `urllib.parse.urlparse` to verify that the URL has a scheme
    ('http' or 'https') and a network location (domain name/IP).

    Args:
        url (str): The string to validate as a URL.

    Returns:
        bool: True if the URL is valid and uses http or https, False otherwise.
    """
    try:
        result = urlparse(url)
        return result.scheme in ["http", "https"] and bool(result.netloc)
    except (ValueError, TypeError):
        return False


def main():
    """
    Initializes and starts the FastMCP server in stdio mode.

    This function serves as the main entry point for running the server
    when the script is executed directly. It listens for requests over
    standard input/output.
    """
    logging.info("Starting FastMCP server with stdio transport...")
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
