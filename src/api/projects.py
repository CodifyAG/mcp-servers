"""
Projects API endpoints for Harvest.
"""
from typing import Dict, Optional
from .core import harvest_api_request

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
    params = {}
    if is_active is not None:
        params["is_active"] = is_active
    if client_id is not None:
        params["client_id"] = client_id
    if updated_since is not None:
        params["updated_since"] = updated_since
    
    params["page"] = page
    params["per_page"] = per_page
    
    return harvest_api_request("GET", "/projects", params=params)


def get_project(project_id: int) -> Dict:
    """
    Retrieves a specific project by its ID.

    Args:
        project_id: The ID of the project to retrieve.

    Returns:
        A dictionary containing the project data, or an error message.
    """
    return harvest_api_request("GET", f"/projects/{project_id}")


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
        "bill_by": bill_by,
        "budget_by": budget_by,
    }
    
    if code is not None:
        data["code"] = code
    if is_active is not None:
        data["is_active"] = is_active
    if is_billable is not None:
        data["is_billable"] = is_billable
    if is_fixed_fee is not None:
        data["is_fixed_fee"] = is_fixed_fee
    if hourly_rate is not None:
        data["hourly_rate"] = hourly_rate
    if budget is not None:
        data["budget"] = budget
    if budget_is_monthly is not None:
        data["budget_is_monthly"] = budget_is_monthly
    if notify_when_over_budget is not None:
        data["notify_when_over_budget"] = notify_when_over_budget
    if over_budget_notification_percentage is not None:
        data["over_budget_notification_percentage"] = over_budget_notification_percentage
    if show_budget_to_all is not None:
        data["show_budget_to_all"] = show_budget_to_all
    if cost_budget is not None:
        data["cost_budget"] = cost_budget
    if cost_budget_include_expenses is not None:
        data["cost_budget_include_expenses"] = cost_budget_include_expenses
    if fee is not None:
        data["fee"] = fee
    if notes is not None:
        data["notes"] = notes
    if starts_on is not None:
        data["starts_on"] = starts_on
    if ends_on is not None:
        data["ends_on"] = ends_on
    
    return harvest_api_request("POST", "/projects", data=data)


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
    data = {}
    if client_id is not None:
        data["client_id"] = client_id
    if name is not None:
        data["name"] = name
    if code is not None:
        data["code"] = code
    if is_active is not None:
        data["is_active"] = is_active
    if is_billable is not None:
        data["is_billable"] = is_billable
    if is_fixed_fee is not None:
        data["is_fixed_fee"] = is_fixed_fee
    if bill_by is not None:
        data["bill_by"] = bill_by
    if hourly_rate is not None:
        data["hourly_rate"] = hourly_rate
    if budget is not None:
        data["budget"] = budget
    if budget_by is not None:
        data["budget_by"] = budget_by
    if budget_is_monthly is not None:
        data["budget_is_monthly"] = budget_is_monthly
    if notify_when_over_budget is not None:
        data["notify_when_over_budget"] = notify_when_over_budget
    if over_budget_notification_percentage is not None:
        data["over_budget_notification_percentage"] = over_budget_notification_percentage
    if show_budget_to_all is not None:
        data["show_budget_to_all"] = show_budget_to_all
    if cost_budget is not None:
        data["cost_budget"] = cost_budget
    if cost_budget_include_expenses is not None:
        data["cost_budget_include_expenses"] = cost_budget_include_expenses
    if fee is not None:
        data["fee"] = fee
    if notes is not None:
        data["notes"] = notes
    if starts_on is not None:
        data["starts_on"] = starts_on
    if ends_on is not None:
        data["ends_on"] = ends_on
    
    return harvest_api_request("PATCH", f"/projects/{project_id}", data=data)


def delete_project(project_id: int) -> Dict:
    """
    Deletes a project.

    Args:
        project_id: The ID of the project to delete.

    Returns:
        A dictionary indicating success or failure.
    """
    return harvest_api_request("DELETE", f"/projects/{project_id}")
