# Brave Search MCP Server

A Model Context Protocol (MCP) server implementation for Brave Search, enabling seamless integration with MCP clients. This project provides a standardized way to interact with Brave Search through the Model Context Protocol.

<!-- Add your badge here when available -->
<!--
<a href="https://glama.ai/mcp/servers/YOUR_SERVER_ID">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/YOUR_SERVER_ID/badge" alt="Server for Brave Search MCP server" />
</a>
-->

## About

This project implements a [Model Context Protocol](https://modelcontextprotocol.io/) server that wraps Brave Search's REST API, allowing MCP clients to interact with Brave Search in a standardized way. It provides access to web search functionality and website content fetching capabilities.

## Setup and Configuration

### Prerequisites

- Python 3.11 or higher
- Brave Search API key (sign up at [Brave Search API](https://brave.com/search/api/))

### Installation

1. Clone the repository:

```bash
git clone https://github.com/your-organization/mcp-servers.git
cd mcp-servers
```

2. Set up environment variables:

```bash
export BRAVE_API_KEY=your-brave-api-key
```

Alternatively, create a `.env` file in the server directory:

```
BRAVE_API_KEY=your-brave-api-key
```

### Running the Server

```bash
cd servers/brave_search
python -m brave_search_mcp
```

### Configuration with Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "mcp-server-brave-search": {
      "command": "python",
      "args": ["-m", "servers.brave_search.brave_search_mcp"],
      "cwd": "/path/to/mcp-servers",
      "env": {
        "BRAVE_API_KEY": "your-brave-api-key"
      }
    }
  }
}
```

### Configuration with Core AI

TBD

## Feature Implementation Status

| Feature               | Status |
| --------------------- | ------ |
| **Web Search**        |        |
| Basic Web Search      | ✅     |
| **Website Content**   |        |
| Fetch Website Content | ✅     |

## API Reference

### Web Search

```python
# Perform a web search
brave_web_search(query: str, count: int = 10, offset: int = 0) -> str
```

Parameters:

- `query`: Search query string (required)
- `count`: Number of results to return (default: 10, max: 20)
- `offset`: Results offset for pagination (default: 0)

Returns:

- A formatted string containing search results with titles, URLs, and descriptions

### Website Content

```python
# Fetch and clean website content
fetch_website(url: str) -> str
```

Parameters:

- `url`: The URL of the website to fetch (required)

Returns:

- Clean text content from the website with scripts, styles, and excessive whitespace removed

## Examples

### Performing a Web Search

```python
# Search for information about a topic
results = brave_web_search(
    query="renewable energy developments",
    count=5
)

# Search with pagination for more results
more_results = brave_web_search(
    query="renewable energy developments",
    count=5,
    offset=5
)
```

### Fetching Website Content

```python
# Fetch and clean content from a website
content = fetch_website(
    url="https://example.com/article"
)
```

## Troubleshooting

### Common Issues

1. **Authentication Errors**: Ensure your Brave API key is correct and has not expired.

2. **Rate Limiting**: Brave Search API has rate limits. If you encounter rate limiting errors, reduce the frequency of your requests.

3. **Invalid Search Parameters**: Ensure all required parameters are provided for each API call.

4. **Invalid URLs**: When using `fetch_website`, ensure you provide valid URLs including the protocol (http/https).

## Development

To set up the development environment:

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

The project includes comprehensive test coverage for all API functionality.

## Contributing

Please see the main [CONTRIBUTING.md](../../../CONTRIBUTING.md) file for details on how to contribute to this project.

## License

This project is licensed under the MIT License - see the [LICENSE](../../../LICENSE) file for details.
