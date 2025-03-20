"""
Core utilities for Harvest API requests.
"""
import os
from typing import Dict, Optional
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration constants
HARVEST_ACCOUNT_ID = os.getenv("HARVEST_ACCOUNT_ID")
HARVEST_ACCESS_TOKEN = os.getenv("HARVEST_ACCESS_TOKEN")
USER_AGENT = "Smart Harvest Tool"

def harvest_api_request(method: str, endpoint: str, data: Optional[Dict] = None, params: Optional[Dict] = None) -> Dict:
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
            method=method,
            url=url,
            headers=headers,
            json=data if data else None,
            params=params if params else None,
        )
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        error_message = str(e)
        try:
            error_json = e.response.json()
            if "message" in error_json:
                error_message = error_json["message"]
        except (ValueError, AttributeError):
            pass
        return {"error": error_message}
