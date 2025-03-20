"""
Time entries API endpoints for Harvest.
"""
from typing import Dict, List, Optional
from .core import harvest_api_request

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
    params = {k: v for k, v in locals().items() if v is not None and k not in ["page", "per_page"]}
    params["page"] = page
    params["per_page"] = per_page
    return harvest_api_request("GET", "/time_entries", params=params)


def get_time_entry(time_entry_id: int) -> Dict:
    """
    Retrieves a specific time entry by its ID.

    Args:
        time_entry_id: The ID of the time entry to retrieve.

    Returns:
        A dictionary containing the time entry data, or an error message.
    """
    return harvest_api_request("GET", f"/time_entries/{time_entry_id}")


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
        user_id: The ID of the user to associate with the time entry. Defaults to the currently authenticated user's ID.
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
        "project_id": project_id,
        "task_id": task_id,
        "spent_date": spent_date,
    }
    
    if user_id is not None:
        data["user_id"] = user_id
    if hours is not None:
        data["hours"] = hours
    if notes is not None:
        data["notes"] = notes
    if external_reference is not None:
        data["external_reference"] = external_reference
        
    return harvest_api_request("POST", "/time_entries", data=data)


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
        user_id: The ID of the user to associate with the time entry. Defaults to the currently authenticated user's ID.
        started_time: The time the entry started. Example: "8:00am".
        ended_time: The time the entry ended. If provided, is_running will be set to false. If not provided, is_running will be set to true.
        notes: Any notes to be associated with the time entry.
        external_reference: An object containing the id, group_id, account_id, and permalink of the external reference.

    Returns:
        A dictionary containing the created time entry data, or an error message.
    """
    data = {
        "project_id": project_id,
        "task_id": task_id,
        "spent_date": spent_date,
    }
    
    if user_id is not None:
        data["user_id"] = user_id
    if started_time is not None:
        data["started_time"] = started_time
    if ended_time is not None:
        data["ended_time"] = ended_time
    if notes is not None:
        data["notes"] = notes
    if external_reference is not None:
        data["external_reference"] = external_reference
        
    return harvest_api_request("POST", "/time_entries", data=data)


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
        started_time: The time the entry started. Example: "8:00am".
        ended_time: The time the entry ended.
        hours: The current amount of time tracked.
        notes: Any notes to be associated with the time entry.
        external_reference: An object containing the id, group_id, account_id, and permalink of the external reference.

    Returns:
        A dictionary containing the updated time entry data, or an error message.
    """
    data = {}
    if project_id is not None:
        data["project_id"] = project_id
    if task_id is not None:
        data["task_id"] = task_id
    if spent_date is not None:
        data["spent_date"] = spent_date
    if started_time is not None:
        data["started_time"] = started_time
    if ended_time is not None:
        data["ended_time"] = ended_time
    if hours is not None:
        data["hours"] = hours
    if notes is not None:
        data["notes"] = notes
    if external_reference is not None:
        data["external_reference"] = external_reference
        
    return harvest_api_request("PATCH", f"/time_entries/{time_entry_id}", data=data)


def delete_time_entry_external_reference(time_entry_id: int) -> Dict:
    """
    Deletes a time entry's external reference.

    Args:
        time_entry_id: The ID of the time entry.

    Returns:
        A dictionary indicating success or failure.
    """
    return harvest_api_request("DELETE", f"/time_entries/{time_entry_id}/external_reference")


def delete_time_entry(time_entry_id: int) -> Dict:
    """
    Deletes a time entry.

    Args:
        time_entry_id: The ID of the time entry to delete.

    Returns:
        A dictionary indicating success or failure.
    """
    return harvest_api_request("DELETE", f"/time_entries/{time_entry_id}")


def restart_time_entry(time_entry_id: int) -> Dict:
    """
    Restarts a stopped time entry.

    Args:
        time_entry_id: The ID of the time entry to restart.

    Returns:
        A dictionary containing the restarted time entry data, or an error message.
    """
    return harvest_api_request("PATCH", f"/time_entries/{time_entry_id}/restart")


def stop_time_entry(time_entry_id: int) -> Dict:
    """
    Stops a running time entry.

    Args:
        time_entry_id: The ID of the time entry to stop.

    Returns:
        A dictionary containing the stopped time entry data, or an error message.
    """
    return harvest_api_request("PATCH", f"/time_entries/{time_entry_id}/stop")
