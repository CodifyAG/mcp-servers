# Harvest MCP Server

A Model Context Protocol (MCP) server implementation for Harvest, enabling seamless integration with MCP clients. This project provides a standardized way to interact with Harvest through the Model Context Protocol.

<!-- Add your badge here when available -->
<!--
<a href="https://glama.ai/mcp/servers/YOUR_SERVER_ID">
  <img width="380" height="200" src="https://glama.ai/mcp/servers/YOUR_SERVER_ID/badge" alt="Server for Harvest Time Tracking MCP server" />
</a>
-->

## About

This project implements a [Model Context Protocol](https://modelcontextprotocol.io/) server that wraps Harvest's REST API, allowing MCP clients to interact with Harvest in a standardized way. It provides access to Harvest's time tracking, client, project, and reporting features.

## Setup and Configuration

### Prerequisites

- Python 3.9 or higher
- Harvest account with API access
- Harvest API credentials (Account ID and Access Token)

### Installation

1. Clone the repository:
```bash
git clone https://github.com/your-organization/mcp-servers.git
cd mcp-servers
```

2. Set up environment variables:
```bash
export HARVEST_ACCOUNT_ID=your-harvest-account-id
export HARVEST_ACCESS_TOKEN=your-harvest-access-token
```

Alternatively, create a `.env` file in the server directory:
```
HARVEST_ACCOUNT_ID=your-harvest-account-id
HARVEST_ACCESS_TOKEN=your-harvest-access-token
```

### Running the Server

```bash
cd servers/harvest
python -m src.server
```

### Configuration with Claude Desktop

Add to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "mcp-server-harvest": {
      "command": "python",
      "args": ["-m", "servers.harvest.src.server"],
      "cwd": "/path/to/mcp-servers",
      "env": {
        "HARVEST_ACCOUNT_ID": "your-harvest-account-id",
        "HARVEST_ACCESS_TOKEN": "your-harvest-access-token"
      }
    }
  }
}
```

### Configuration with Core AI

TBD

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

## API Reference

### Time Entries

```python
# List time entries
list_time_entries(user_id=None, client_id=None, project_id=None, ...)

# Get a specific time entry
get_time_entry(time_entry_id)

# Create a time entry with duration
create_time_entry_duration(project_id, task_id, spent_date, ...)

# Create a time entry with start/end times
create_time_entry_start_end(project_id, task_id, spent_date, ...)
```

### Clients

```python
# List clients
list_clients(is_active=None, updated_since=None, ...)

# Get a specific client
get_client(client_id)

# Create a client
create_client(name, is_active=None, address=None, ...)
```

### Projects

```python
# List projects
list_projects(is_active=None, client_id=None, ...)

# Get a specific project
get_project(project_id)

# Create a project
create_project(client_id, name, ...)
```

### Reports

```python
# Get clients time report
get_clients_time_report(from_date, to_date, ...)

# Get projects time report
get_projects_time_report(from_date, to_date, ...)
```

## Examples

### Tracking Time

```python
# Create a new time entry for today
create_time_entry_duration(
    project_id=12345,
    task_id=67890,
    spent_date="2025-03-24",
    hours=2.5,
    notes="Working on documentation"
)

# List time entries for a specific date range
entries = list_time_entries(
    from_date="2025-03-01",
    to_date="2025-03-31"
)
```

### Managing Clients

```python
# Create a new client
create_client(
    name="ACME Corporation",
    address="123 Main St, Anytown, USA"
)

# List all active clients
clients = list_clients(is_active=True)
```

## Troubleshooting

### Common Issues

1. **Authentication Errors**: Ensure your Harvest API credentials are correct and have the necessary permissions.

2. **Rate Limiting**: Harvest API has rate limits. If you encounter rate limiting errors, reduce the frequency of your requests.

3. **Missing Data**: Ensure all required parameters are provided for each API call.

## Contributing

Please see the main [CONTRIBUTING.md](../../../CONTRIBUTING.md) file for details on how to contribute to this project.

## License

This project is licensed under the MIT License - see the [LICENSE](../../../LICENSE) file for details.
