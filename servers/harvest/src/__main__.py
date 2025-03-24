import json
import os
from typing import Dict, List, Optional

import requests
from dotenv import load_dotenv
from mcp.server.fastmcp import FastMCP

# Load environment variables
load_dotenv()

# Configuration constants
HARVEST_ACCOUNT_ID = os.getenv("HARVEST_ACCOUNT_ID")
HARVEST_ACCESS_TOKEN = os.getenv("HARVEST_ACCESS_TOKEN")
USER_AGENT = "Smart Harvest Tool"

# Initialize FastMCP
mcp = FastMCP("Smart Harvest Tool")


# Utility function to make Harvest API requests
def harvest_api_request(
    method: str,
    endpoint: str,
    data: Optional[Dict] = None,
    params: Optional[Dict] = None,
) -> Dict:
    """
    Makes a request to the Harvest API.

    Args:
        method: HTTP method (GET, POST, PATCH, DELETE).
        endpoint: API endpoint (e.g., "/time_entries").
        data: Request body (for POST, PATCH).
        params: Query parameters (for GET).

    Returns:
        A dictionary containing the JSON response from the API, or an error message.
    """
    base_url = "https://api.harvestapp.com/v2"
    url = f"{base_url}{endpoint}"
    headers = {
        "Authorization": f"Bearer {HARVEST_ACCESS_TOKEN}",
        "Harvest-Account-Id": HARVEST_ACCOUNT_ID,
        "User-Agent": USER_AGENT,
        "Content-Type": "application/json",
    }

    try:
        response = requests.request(
            method, url, headers=headers, json=data, params=params
        )
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        return response.json()
    except requests.exceptions.RequestException as e:
        return {"success": False, "error": str(e)}


@mcp.tool()
def list_time_entries(
    user_id: Optional[int] = None,
    client_id: Optional[int] = None,
    project_id: Optional[int] = None,
    task_id: Optional[int] = None,
    external_reference_id: Optional[str] = None,
    is_billed: Optional[bool] = None,
    is_running: Optional[bool] = None,
    updated_since: Optional[str] = None,
    from_date: Optional[str] = None,
    to_date: Optional[str] = None,
    page: Optional[int] = 1,
    per_page: Optional[int] = 2000,
) -> Dict:
    """
    Retrieves a list of time entries with optional filters.

    Args:
        user_id: Only return time entries belonging to the user with the given ID.
        client_id: Only return time entries belonging to the client with the given ID.
        project_id: Only return time entries belonging to the project with the given ID.
        task_id: Only return time entries belonging to the task with the given ID.
        external_reference_id: Only return time entries with the given external_reference ID.
        is_billed: Pass true to only return time entries that have been invoiced and false to return time entries that have not been invoiced.
        is_running: Pass true to only return running time entries and false to return non-running time entries.
        updated_since: Only return time entries that have been updated since the given date and time (ISO 8601 format).
        from_date: Only return time entries with a spent_date on or after the given date.
        to_date: Only return time entries with a spent_date on or before the given date.
        page: The page number to use in pagination.
        per_page: The number of records to return per page. Can range between 1 and 2000.

    Returns:
        A dictionary containing the list of time entries, pagination information, or an error message.
    """
    params = {
        "user_id": user_id,
        "client_id": client_id,
        "project_id": project_id,
        "task_id": task_id,
        "external_reference_id": external_reference_id,
        "is_billed": is_billed,
        "is_running": is_running,
        "updated_since": updated_since,
        "from": from_date,
        "to": to_date,
        "page": page,
        "per_page": per_page,
    }

    response = harvest_api_request("GET", "/time_entries", params=params)

    if "time_entries" in response:
        return response
    else:
        return response  # Return the error response


@mcp.tool()
def get_time_entry(time_entry_id: int) -> Dict:
    """
    Retrieves a specific time entry by its ID.

    Args:
        time_entry_id: The ID of the time entry to retrieve.

    Returns:
        A dictionary containing the time entry data, or an error message.
    """
    response = harvest_api_request("GET", f"/time_entries/{time_entry_id}")
    return response


@mcp.tool()
def create_time_entry_duration(
    project_id: int,
    task_id: int,
    spent_date: str,
    user_id: Optional[int] = None,
    hours: Optional[float] = None,
    notes: Optional[str] = None,
    external_reference: Optional[Dict] = None,
) -> Dict:
    """
    Creates a new time entry using duration.

    Args:
        user_id: The ID of the user to associate with the time entry. Defaults to the currently authenticated user’s ID.
        project_id: The ID of the project to associate with the time entry.
        task_id: The ID of the task to associate with the time entry.
        spent_date: The ISO 8601 formatted date the time entry was spent.
        hours: The current amount of time tracked. If provided, the time entry will be created with the specified hours and is_running will be set to false. If not provided, hours will be set to 0.0 and is_running will be set to true.
        notes: Any notes to be associated with the time entry.
        external_reference: An object containing the id, group_id, account_id, and permalink of the external reference.

    Returns:
        A dictionary containing the created time entry data, or an error message.
    """
    data = {
        "user_id": user_id,
        "project_id": project_id,
        "task_id": task_id,
        "spent_date": spent_date,
        "hours": hours,
        "notes": notes,
        "external_reference": external_reference,
    }
    response = harvest_api_request("POST", "/time_entries", data=data)
    return response


@mcp.tool()
def create_time_entry_start_end(
    project_id: int,
    task_id: int,
    spent_date: str,
    user_id: Optional[int] = None,
    started_time: Optional[str] = None,
    ended_time: Optional[str] = None,
    notes: Optional[str] = None,
    external_reference: Optional[Dict] = None,
) -> Dict:
    """
    Creates a new time entry using start and end times.

    Args:
        project_id: The ID of the project to associate with the time entry.
        task_id: The ID of the task to associate with the time entry.
        spent_date: The ISO 8601 formatted date the time entry was spent.
        user_id: The ID of the user to associate with the time entry. Defaults to the currently authenticated user’s ID.
        started_time: The time the entry started. Example: “8:00am”.
        ended_time: The time the entry ended. If provided, is_running will be set to false. If not provided, is_running will be set to true.
        notes: Any notes to be associated with the time entry.
        external_reference: An object containing the id, group_id, account_id, and permalink of the external reference.

    Returns:
        A dictionary containing the created time entry data, or an error message.
    """
    data = {
        "user_id": user_id,
        "project_id": project_id,
        "task_id": task_id,
        "spent_date": spent_date,
        "started_time": started_time,
        "ended_time": ended_time,
        "notes": notes,
        "external_reference": external_reference,
    }
    response = harvest_api_request("POST", "/time_entries", data=data)
    return response


@mcp.tool()
def update_time_entry(
    time_entry_id: int,
    project_id: Optional[int] = None,
    task_id: Optional[int] = None,
    spent_date: Optional[str] = None,
    started_time: Optional[str] = None,
    ended_time: Optional[str] = None,
    hours: Optional[float] = None,
    notes: Optional[str] = None,
    external_reference: Optional[Dict] = None,
) -> Dict:
    """
    Updates an existing time entry.

    Args:
        time_entry_id: The ID of the time entry to update.
        project_id: The ID of the project to associate with the time entry.
        task_id: The ID of the task to associate with the time entry.
        spent_date: The ISO 8601 formatted date the time entry was spent.
        started_time: The time the entry started. Example: “8:00am”.
        ended_time: The time the entry ended.
        hours: The current amount of time tracked.
        notes: Any notes to be associated with the time entry.
        external_reference: An object containing the id, group_id, account_id, and permalink of the external reference.

    Returns:
        A dictionary containing the updated time entry data, or an error message.
    """
    data = {
        "project_id": project_id,
        "task_id": task_id,
        "spent_date": spent_date,
        "started_time": started_time,
        "ended_time": ended_time,
        "hours": hours,
        "notes": notes,
        "external_reference": external_reference,
    }
    response = harvest_api_request("PATCH", f"/time_entries/{time_entry_id}", data=data)
    return response


@mcp.tool()
def delete_time_entry_external_reference(time_entry_id: int) -> Dict:
    """
    Deletes a time entry’s external reference.

    Args:
        time_entry_id: The ID of the time entry.

    Returns:
        A dictionary indicating success or failure.
    """
    response = harvest_api_request(
        "DELETE", f"/time_entries/{time_entry_id}/external_reference"
    )
    return response


@mcp.tool()
def delete_time_entry(time_entry_id: int) -> Dict:
    """
    Deletes a time entry.

    Args:
        time_entry_id: The ID of the time entry to delete.

    Returns:
        A dictionary indicating success or failure.
    """
    response = harvest_api_request("DELETE", f"/time_entries/{time_entry_id}")
    return response


@mcp.tool()
def restart_time_entry(time_entry_id: int) -> Dict:
    """
    Restarts a stopped time entry.

    Args:
        time_entry_id: The ID of the time entry to restart.

    Returns:
        A dictionary containing the restarted time entry data, or an error message.
    """
    response = harvest_api_request("PATCH", f"/time_entries/{time_entry_id}/restart")
    return response


@mcp.tool()
def stop_time_entry(time_entry_id: int) -> Dict:
    """
    Stops a running time entry.

    Args:
        time_entry_id: The ID of the time entry to stop.

    Returns:
        A dictionary containing the stopped time entry data, or an error message.
    """
    response = harvest_api_request("PATCH", f"/time_entries/{time_entry_id}/stop")
    return response


@mcp.tool()
def list_clients(
    is_active: Optional[bool] = None,
    updated_since: Optional[str] = None,
    page: Optional[int] = 1,
    per_page: Optional[int] = 2000,
) -> Dict:
    """
    Retrieves a list of clients.

    Args:
        is_active: Pass true to only return active clients and false to return inactive clients.
        updated_since: Only return clients that have been updated since the given date and time.
        page: DEPRECATED The page number to use in pagination.
        per_page: The number of records to return per page. Can range between 1 and 2000.

    Returns:
        A dictionary containing the list of clients, pagination information, or an error message.
    """
    params = {
        "is_active": is_active,
        "updated_since": updated_since,
        "page": page,
        "per_page": per_page,
    }

    response = harvest_api_request("GET", "/clients", params=params)

    if "clients" in response:
        return response
    else:
        return response  # Return the error response


@mcp.tool()
def get_client(client_id: int) -> Dict:
    """
    Retrieves a specific client by its ID.

    Args:
        client_id: The ID of the client to retrieve.

    Returns:
        A dictionary containing the client data, or an error message.
    """
    response = harvest_api_request("GET", f"/clients/{client_id}")
    return response


@mcp.tool()
def create_client(
    name: str,
    is_active: Optional[bool] = None,
    address: Optional[str] = None,
    currency: Optional[str] = None,
) -> Dict:
    """
    Creates a new client.

    Args:
        name: A textual description of the client.
        is_active: Whether the client is active, or archived. Defaults to true.
        address: A textual representation of the client’s physical address. May include new line characters.
        currency: The currency used by the client. If not provided, the company’s currency will be used.

    Returns:
        A dictionary containing the created client data, or an error message.
    """
    data = {
        "name": name,
        "is_active": is_active,
        "address": address,
        "currency": currency,
    }
    response = harvest_api_request("POST", "/clients", data=data)
    return response


@mcp.tool()
def update_client(
    client_id: int,
    name: Optional[str] = None,
    is_active: Optional[bool] = None,
    address: Optional[str] = None,
    currency: Optional[str] = None,
) -> Dict:
    """
    Updates an existing client.

    Args:
        client_id: The ID of the client to update.
        name: A textual description of the client.
        is_active: Whether the client is active, or archived.
        address: A textual representation of the client’s physical address. May include new line characters.
        currency: The currency used by the client.

    Returns:
        A dictionary containing the updated client data, or an error message.
    """
    data = {
        "name": name,
        "is_active": is_active,
        "address": address,
        "currency": currency,
    }
    response = harvest_api_request("PATCH", f"/clients/{client_id}", data=data)
    return response


@mcp.tool()
def delete_client(client_id: int) -> Dict:
    """
    Deletes a client.

    Args:
        client_id: The ID of the client to delete.

    Returns:
        A dictionary indicating success or failure.
    """
    response = harvest_api_request("DELETE", f"/clients/{client_id}")
    return response


@mcp.tool()
def list_projects(
    is_active: Optional[bool] = None,
    client_id: Optional[int] = None,
    updated_since: Optional[str] = None,
    page: Optional[int] = 1,
    per_page: Optional[int] = 2000,
) -> Dict:
    """
    Retrieves a list of projects.

    Args:
        is_active: Pass true to only return active projects and false to return inactive projects.
        client_id: Only return projects belonging to the client with the given ID.
        updated_since: Only return projects that have been updated since the given date and time.
        page: DEPRECATED The page number to use in pagination.
        per_page: The number of records to return per page.

    Returns:
        A dictionary containing the list of projects, pagination information, or an error message.
    """
    params = {
        "is_active": is_active,
        "client_id": client_id,
        "updated_since": updated_since,
        "page": page,
        "per_page": per_page,
    }

    response = harvest_api_request("GET", "/projects", params=params)

    if "projects" in response:
        return response
    else:
        return response  # Return the error response


@mcp.tool()
def get_project(project_id: int) -> Dict:
    """
    Retrieves a specific project by its ID.

    Args:
        project_id: The ID of the project to retrieve.

    Returns:
        A dictionary containing the project data, or an error message.
    """
    response = harvest_api_request("GET", f"/projects/{project_id}")
    return response


@mcp.tool()
def create_project(
    client_id: int,
    name: str,
    code: Optional[str] = None,
    is_active: Optional[bool] = None,
    is_billable: Optional[bool] = None,
    is_fixed_fee: Optional[bool] = None,
    bill_by: str = "Project",
    hourly_rate: Optional[float] = None,
    budget: Optional[float] = None,
    budget_by: str = "project",
    budget_is_monthly: Optional[bool] = None,
    notify_when_over_budget: Optional[bool] = None,
    over_budget_notification_percentage: Optional[float] = None,
    show_budget_to_all: Optional[bool] = None,
    cost_budget: Optional[float] = None,
    cost_budget_include_expenses: Optional[bool] = None,
    fee: Optional[float] = None,
    notes: Optional[str] = None,
    starts_on: Optional[str] = None,
    ends_on: Optional[str] = None,
) -> Dict:
    """
    Creates a new project.

    Args:
        client_id: The ID of the client to associate this project with.
        name: The name of the project.
        code: The code associated with the project.
        is_active: Whether the project is active or archived. Defaults to true.
        is_billable: Whether the project is billable or not.
        is_fixed_fee: Whether the project is a fixed-fee project or not.
        bill_by: The method by which the project is invoiced. Options: Project, Tasks, People, or none.
        hourly_rate: Rate for projects billed by Project Hourly Rate.
        budget: The budget in hours for the project when budgeting by time.
        budget_by: The method by which the project is budgeted. Options: project (Hours Per Project), project_cost (Total Project Fees), task (Hours Per Task), task_fees (Fees Per Task), person (Hours Per Person), none (No Budget).
        budget_is_monthly: Option to have the budget reset every month. Defaults to false.
        notify_when_over_budget: Whether Project Managers should be notified when the project goes over budget. Defaults to false.
        over_budget_notification_percentage: Percentage value used to trigger over budget email alerts. Example: use 10.0 for 10.0%.
        show_budget_to_all: Option to show project budget to all employees. Does not apply to Total Project Fee projects. Defaults to false.
        cost_budget: The monetary budget for the project when budgeting by money.
        cost_budget_include_expenses: Option for budget of Total Project Fees projects to include tracked expenses. Defaults to false.
        fee: The amount you plan to invoice for the project. Only used by fixed-fee projects.
        notes: Project notes.
        starts_on: Date the project was started.
        ends_on: Date the project will end.

    Returns:
        A dictionary containing the created project data, or an error message.
    """
    data = {
        "client_id": client_id,
        "name": name,
        "code": code,
        "is_active": is_active,
        "is_billable": is_billable,
        "is_fixed_fee": is_fixed_fee,
        "bill_by": bill_by,
        "hourly_rate": hourly_rate,
        "budget": budget,
        "budget_by": budget_by,
        "budget_is_monthly": budget_is_monthly,
        "notify_when_over_budget": notify_when_over_budget,
        "over_budget_notification_percentage": over_budget_notification_percentage,
        "show_budget_to_all": show_budget_to_all,
        "cost_budget": cost_budget,
        "cost_budget_include_expenses": cost_budget_include_expenses,
        "fee": fee,
        "notes": notes,
        "starts_on": starts_on,
        "ends_on": ends_on,
    }
    response = harvest_api_request("POST", "/projects", data=data)
    return response


@mcp.tool()
def update_project(
    project_id: int,
    client_id: Optional[int] = None,
    name: Optional[str] = None,
    code: Optional[str] = None,
    is_active: Optional[bool] = None,
    is_billable: Optional[bool] = None,
    is_fixed_fee: Optional[bool] = None,
    bill_by: Optional[str] = None,
    hourly_rate: Optional[float] = None,
    budget: Optional[float] = None,
    budget_by: Optional[str] = None,
    budget_is_monthly: Optional[bool] = None,
    notify_when_over_budget: Optional[bool] = None,
    over_budget_notification_percentage: Optional[float] = None,
    show_budget_to_all: Optional[bool] = None,
    cost_budget: Optional[float] = None,
    cost_budget_include_expenses: Optional[bool] = None,
    fee: Optional[float] = None,
    notes: Optional[str] = None,
    starts_on: Optional[str] = None,
    ends_on: Optional[str] = None,
) -> Dict:
    """
    Updates an existing project.

    Args:
        project_id: The ID of the project to update.
        client_id: The ID of the client to associate this project with.
        name: The name of the project.
        code: The code associated with the project.
        is_active: Whether the project is active or archived.
        is_billable: Whether the project is billable or not.
        is_fixed_fee: Whether the project is a fixed-fee project or not.
        bill_by: The method by which the project is invoiced. Options: Project, Tasks, People, or none.
        hourly_rate: Rate for projects billed by Project Hourly Rate.
        budget: The budget in hours for the project when budgeting by time.
        budget_by: The method by which the project is budgeted. Options: project (Hours Per Project), project_cost (Total Project Fees), task (Hours Per Task), task_fees (Fees Per Task), person (Hours Per Person), none (No Budget).
        budget_is_monthly: Option to have the budget reset every month.
        notify_when_over_budget: Whether Project Managers should be notified when the project goes over budget.
        over_budget_notification_percentage: Percentage value used to trigger over budget email alerts. Example: use 10.0 for 10.0%.
        show_budget_to_all: Option to show project budget to all employees. Does not apply to Total Project Fee projects.
        cost_budget: The monetary budget for the project when budgeting by money.
        cost_budget_include_expenses: Option for budget of Total Project Fees projects to include tracked expenses.
        fee: The amount you plan to invoice for the project. Only used by fixed-fee projects.
        notes: Project notes.
        starts_on: Date the project was started.
        ends_on: Date the project will end.

    Returns:
        A dictionary containing the updated project data, or an error message.
    """
    data = {
        "client_id": client_id,
        "name": name,
        "code": code,
        "is_active": is_active,
        "is_billable": is_billable,
        "is_fixed_fee": is_fixed_fee,
        "bill_by": bill_by,
        "hourly_rate": hourly_rate,
        "budget": budget,
        "budget_by": budget_by,
        "budget_is_monthly": budget_is_monthly,
        "notify_when_over_budget": notify_when_over_budget,
        "over_budget_notification_percentage": over_budget_notification_percentage,
        "show_budget_to_all": show_budget_to_all,
        "cost_budget": cost_budget,
        "cost_budget_include_expenses": cost_budget_include_expenses,
        "fee": fee,
        "notes": notes,
        "starts_on": starts_on,
        "ends_on": ends_on,
    }
    response = harvest_api_request("PATCH", f"/projects/{project_id}", data=data)
    return response


@mcp.tool()
def delete_project(project_id: int) -> Dict:
    """
    Deletes a project.

    Args:
        project_id: The ID of the project to delete.

    Returns:
        A dictionary indicating success or failure.
    """
    response = harvest_api_request("DELETE", f"/projects/{project_id}")
    return response


@mcp.tool()
def get_clients_time_report(
    from_date: str,
    to_date: str,
    include_fixed_fee: Optional[bool] = None,
    page: Optional[int] = 1,
    per_page: Optional[int] = 2000,
) -> Dict:
    """
    Retrieves a clients time report.

    Args:
        from_date: Only report on time entries with a spent_date on or after the given date.
        to_date: Only report on time entries with a spent_date on or before the given date.
        include_fixed_fee: When true, billable amounts will be calculated and included for fixed fee projects.
        page: The page number to use in pagination.
        per_page: The number of records to return per page.

    Returns:
        A dictionary containing the clients time report data, or an error message.
    """
    params = {
        "from": from_date,
        "to": to_date,
        "include_fixed_fee": include_fixed_fee,
        "page": page,
        "per_page": per_page,
    }
    response = harvest_api_request("GET", "/reports/time/clients", params=params)
    return response


@mcp.tool()
def get_projects_time_report(
    from_date: str,
    to_date: str,
    include_fixed_fee: Optional[bool] = None,
    page: Optional[int] = 1,
    per_page: Optional[int] = 2000,
) -> Dict:
    """
    Retrieves a projects time report.

    Args:
        from_date: Only report on time entries with a spent_date on or after the given date.
        to_date: Only report on time entries with a spent_date on or before the given date.
        include_fixed_fee: When true, billable amounts will be calculated and included for fixed fee projects.
        page: The page number to use in pagination.
        per_page: The number of records to return per page.

    Returns:
        A dictionary containing the projects time report data, or an error message.
    """
    params = {
        "from": from_date,
        "to": to_date,
        "include_fixed_fee": include_fixed_fee,
        "page": page,
        "per_page": per_page,
    }
    response = harvest_api_request("GET", "/reports/time/projects", params=params)
    return response


@mcp.tool()
def get_tasks_time_report(
    from_date: str,
    to_date: str,
    include_fixed_fee: Optional[bool] = None,
    page: Optional[int] = 1,
    per_page: Optional[int] = 2000,
) -> Dict:
    """
    Retrieves a tasks time report.

    Args:
        from_date: Only report on time entries with a spent_date on or after the given date.
        to_date: Only report on time entries with a spent_date on or before the given date.
        include_fixed_fee: When true, billable amounts will be calculated and included for fixed fee projects.
        page: The page number to use in pagination.
        per_page: The number of records to return per page.

    Returns:
        A dictionary containing the tasks time report data, or an error message.
    """
    params = {
        "from": from_date,
        "to": to_date,
        "include_fixed_fee": include_fixed_fee,
        "page": page,
        "per_page": per_page,
    }
    response = harvest_api_request("GET", "/reports/time/tasks", params=params)
    return response


@mcp.tool()
def get_team_time_report(
    from_date: str,
    to_date: str,
    include_fixed_fee: Optional[bool] = None,
    page: Optional[int] = 1,
    per_page: Optional[int] = 2000,
) -> Dict:
    """
    Retrieves a team time report.

    Args:
        from_date: Only report on time entries with a spent_date on or after the given date.
        to_date: Only report on time entries with a spent_date on or before the given date.
        include_fixed_fee: When true, billable amounts will be calculated and included for fixed fee projects.
        page: The page number to use in pagination.
        per_page: The number of records to return per page.

    Returns:
        A dictionary containing the team time report data, or an error message.
    """
    params = {
        "from": from_date,
        "to": to_date,
        "include_fixed_fee": include_fixed_fee,
        "page": page,
        "per_page": per_page,
    }
    response = harvest_api_request("GET", "/reports/time/team", params=params)
    return response


if __name__ == "__main__":
    mcp.run(transport="stdio")
