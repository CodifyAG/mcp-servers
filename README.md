# mcp-server-harvest-time-tracking

A Model Context Protocol (MCP) server implementation for Harvest, enabling seamless integration with MCP clients. This project provides a standardized way to interact with Harvest through the Model Context Protocol. This is essentially a wrapper for the Harvest API in MCP format.

<!-- Add your badge here when available -->
<!--
<a href="https://glama.ai/mcp/servers/YOUR_SERVER_ID">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/YOUR_SERVER_ID/badge" alt="Server for Harvest Time Tracking MCP server" />
</a>
-->

## About

This project implements a [Model Context Protocol](https://modelcontextprotocol.io/introduction) server that wraps Harvest's REST API, allowing MCP clients to interact with Harvest in a standardized way. It provides access to Harvest's time tracking, client, project, and reporting features.

## Feature Implementation Status

| Feature | Status |
|---------|--------|
| **Time Entries** | |
| List Time Entries | ✅ |
| Get Time Entry | ✅ |
| Create Time Entry (Duration) | ✅ |
| Create Time Entry (Start/End) | ✅ |
| Update Time Entry | ✅ |
| Delete Time Entry | ✅ |
| Delete Time Entry External Reference | ✅ |
| Restart Time Entry | ✅ |
| Stop Time Entry | ✅ |
| **Clients** | |
| List Clients | ✅ |
| Get Client | ✅ |
| Create Client | ✅ |
| Update Client | ✅ |
| Delete Client | ✅ |
| **Projects** | |
| List Projects | ✅ |
| Get Project | ✅ |
| Create Project | ✅ |
| Update Project | ✅ |
| Delete Project | ✅ |
| **Reports** | |
| Get Clients Time Report | ✅ |
| Get Projects Time Report | ✅ |
| Get Tasks Time Report | ✅ |
| Get Team Time Report | ✅ |

## Project Structure

The project is organized into modules by resource type:

```
src/
├── api/
│   ├── __init__.py
│   ├── core.py           # Core API request functionality
│   ├── time_entries.py   # Time entries endpoints
│   ├── clients.py        # Client management endpoints
│   ├── projects.py       # Project management endpoints
│   └── reports.py        # Time reporting endpoints
└── server.py             # MCP server implementation
```

## Setup

### Dependencies

This project depends on the following packages:
- `mcp`: Model Context Protocol implementation
- `requests`: For making HTTP requests to the Harvest API
- `python-dotenv`: For loading environment variables

### Environment Variables

Set the following environment variables:
```
HARVEST_ACCOUNT_ID=<your-harvest-account-id>
HARVEST_ACCESS_TOKEN=<your-harvest-access-token>
```

You can obtain these credentials from your Harvest account settings or by creating a new OAuth2 application in Harvest.

### Installation

1. Clone the repository:
```bash
git clone https://github.com/your-username/mcp-server-harvest-time-tracking.git
cd mcp-server-harvest-time-tracking
```

2. Set up a virtual environment and install dependencies:
```bash
make setup
```

### Usage with Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "mcp-server-harvest-time-tracking": {
      "command": "python",
      "args": ["-m", "src.server"],
      "cwd": "/path/to/mcp-server-harvest-time-tracking",
      "env": {
        "HARVEST_ACCOUNT_ID": "your-harvest-account-id",
        "HARVEST_ACCESS_TOKEN": "your-harvest-access-token"
      }
    }
  }
}
```

Replace `/path/to/mcp-server-harvest-time-tracking` with the actual path where you've cloned the repository.

### Manual Execution

You can run the server manually:
```bash
make run
```

Options in the Makefile:
- `setup`: Set up the virtual environment and install dependencies
- `run`: Run the server in stdio mode (default)
- `test`: Run tests
- `clean`: Clean up temporary files and virtual environment

## API Usage Examples

### Time Entries

```python
# List time entries
time_entries = list_time_entries(user_id=123, from_date="2023-01-01")

# Create a time entry with duration
entry = create_time_entry_duration(
    project_id=456,
    task_id=789,
    spent_date="2023-01-15",
    hours=2.5,
    notes="Working on documentation"
)

# Stop a running time entry
result = stop_time_entry(time_entry_id=12345)
```

### Projects

```python
# List all active projects
projects = list_projects(is_active=True)

# Get project details
project = get_project(project_id=456)

# Create a new project
new_project = create_project(
    client_id=123,
    name="New Website Development",
    code="NWD-2023",
    is_billable=True
)
```

### Reports

```python
# Get time report for all projects
report = get_projects_time_report(
    from_date="2023-01-01",
    to_date="2023-01-31"
)
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

[MIT License](LICENSE)
