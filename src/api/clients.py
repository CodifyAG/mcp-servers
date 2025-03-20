"""
Clients API endpoints for Harvest.
"""
from typing import Dict, Optional
from .core import harvest_api_request

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
    params = {}
    if is_active is not None:
        params["is_active"] = is_active
    if updated_since is not None:
        params["updated_since"] = updated_since
    
    params["page"] = page
    params["per_page"] = per_page
    
    return harvest_api_request("GET", "/clients", params=params)


def get_client(client_id: int) -> Dict:
    """
    Retrieves a specific client by its ID.

    Args:
        client_id: The ID of the client to retrieve.

    Returns:
        A dictionary containing the client data, or an error message.
    """
    return harvest_api_request("GET", f"/clients/{client_id}")


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
        address: A textual representation of the client's physical address. May include new line characters.
        currency: The currency used by the client. If not provided, the company's currency will be used.

    Returns:
        A dictionary containing the created client data, or an error message.
    """
    data = {"name": name}
    
    if is_active is not None:
        data["is_active"] = is_active
    if address is not None:
        data["address"] = address
    if currency is not None:
        data["currency"] = currency
    
    return harvest_api_request("POST", "/clients", data=data)


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
        address: A textual representation of the client's physical address. May include new line characters.
        currency: The currency used by the client.

    Returns:
        A dictionary containing the updated client data, or an error message.
    """
    data = {}
    if name is not None:
        data["name"] = name
    if is_active is not None:
        data["is_active"] = is_active
    if address is not None:
        data["address"] = address
    if currency is not None:
        data["currency"] = currency
    
    return harvest_api_request("PATCH", f"/clients/{client_id}", data=data)


def delete_client(client_id: int) -> Dict:
    """
    Deletes a client.

    Args:
        client_id: The ID of the client to delete.

    Returns:
        A dictionary indicating success or failure.
    """
    return harvest_api_request("DELETE", f"/clients/{client_id}")
