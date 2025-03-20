"""
Harvest Time Tracking MCP Server.

This server provides an interface to the Harvest API for time tracking.
"""
import os
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Import API modules
from .api.core import harvest_api_request
from .api.time_entries import (
    list_time_entries, get_time_entry, create_time_entry_duration,
    create_time_entry_start_end, update_time_entry, delete_time_entry_external_reference,
    delete_time_entry, restart_time_entry, stop_time_entry
)
from .api.clients import (
    list_clients, get_client, create_client, update_client, delete_client
)
from .api.projects import (
    list_projects, get_project, create_project, update_project, delete_project
)
from .api.reports import (
    get_clients_time_report, get_projects_time_report, 
    get_tasks_time_report, get_team_time_report
)

# Load environment variables
load_dotenv()

# Initialize FastMCP
# Run on specific port
# mcp = FastMCP("Smart Harvest Tool", port=8080)
mcp = FastMCP("Smart Harvest Tool")

# Expose Time Entries endpoints
@mcp.tool()
def list_time_entries_handler(**kwargs):
    return list_time_entries(**kwargs)

@mcp.tool()
def get_time_entry_handler(time_entry_id: int):
    return get_time_entry(time_entry_id)

@mcp.tool()
def create_time_entry_duration_handler(**kwargs):
    return create_time_entry_duration(**kwargs)

@mcp.tool()
def create_time_entry_start_end_handler(**kwargs):
    return create_time_entry_start_end(**kwargs)

@mcp.tool()
def update_time_entry_handler(time_entry_id: int, **kwargs):
    return update_time_entry(time_entry_id, **kwargs)

@mcp.tool()
def delete_time_entry_external_reference_handler(time_entry_id: int):
    return delete_time_entry_external_reference(time_entry_id)

@mcp.tool()
def delete_time_entry_handler(time_entry_id: int):
    return delete_time_entry(time_entry_id)

@mcp.tool()
def restart_time_entry_handler(time_entry_id: int):
    return restart_time_entry(time_entry_id)

@mcp.tool()
def stop_time_entry_handler(time_entry_id: int):
    return stop_time_entry(time_entry_id)

# Expose Clients endpoints
@mcp.tool()
def list_clients_handler(**kwargs):
    return list_clients(**kwargs)

@mcp.tool()
def get_client_handler(client_id: int):
    return get_client(client_id)

@mcp.tool()
def create_client_handler(**kwargs):
    return create_client(**kwargs)

@mcp.tool()
def update_client_handler(client_id: int, **kwargs):
    return update_client(client_id, **kwargs)

@mcp.tool()
def delete_client_handler(client_id: int):
    return delete_client(client_id)

# Expose Projects endpoints
@mcp.tool()
def list_projects_handler(**kwargs):
    return list_projects(**kwargs)

@mcp.tool()
def get_project_handler(project_id: int):
    return get_project(project_id)

@mcp.tool()
def create_project_handler(**kwargs):
    return create_project(**kwargs)

@mcp.tool()
def update_project_handler(project_id: int, **kwargs):
    return update_project(project_id, **kwargs)

@mcp.tool()
def delete_project_handler(project_id: int):
    return delete_project(project_id)

# Expose Reports endpoints
@mcp.tool()
def get_clients_time_report_handler(**kwargs):
    return get_clients_time_report(**kwargs)

@mcp.tool()
def get_projects_time_report_handler(**kwargs):
    return get_projects_time_report(**kwargs)

@mcp.tool()
def get_tasks_time_report_handler(**kwargs):
    return get_tasks_time_report(**kwargs)

@mcp.tool()
def get_team_time_report_handler(**kwargs):
    return get_team_time_report(**kwargs)

if __name__ == "__main__":
    # Run in sse mode e.g. on port 8080 in docker
    # mcp.run(transport="sse")
    mcp.run(transport="stdio")
