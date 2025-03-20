"""
Reports API endpoints for Harvest.
"""
from typing import Dict, Optional
from .core import harvest_api_request

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
        "page": page,
        "per_page": per_page,
    }
    
    if include_fixed_fee is not None:
        params["include_fixed_fee"] = include_fixed_fee
    
    return harvest_api_request("GET", "/reports/time/clients", params=params)


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
        "page": page,
        "per_page": per_page,
    }
    
    if include_fixed_fee is not None:
        params["include_fixed_fee"] = include_fixed_fee
    
    return harvest_api_request("GET", "/reports/time/projects", params=params)


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
        "page": page,
        "per_page": per_page,
    }
    
    if include_fixed_fee is not None:
        params["include_fixed_fee"] = include_fixed_fee
    
    return harvest_api_request("GET", "/reports/time/tasks", params=params)


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
        "page": page,
        "per_page": per_page,
    }
    
    if include_fixed_fee is not None:
        params["include_fixed_fee"] = include_fixed_fee
    
    return harvest_api_request("GET", "/reports/time/team", params=params)
