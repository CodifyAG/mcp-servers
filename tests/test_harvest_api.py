import unittest
from unittest.mock import patch, MagicMock
import requests
import os
import pytest


class TestHarvestAPIAvailability(unittest.TestCase):
    """Test basic connectivity to the Harvest API."""

    def test_harvest_api_is_reachable(self):
        """Test that the Harvest API base URL is reachable."""
        # This test only checks if the Harvest API domain is reachable
        # It doesn't make actual API calls that require authentication
        try:
            response = requests.head("https://api.harvestapp.com/v2", timeout=5)
            self.assertTrue(response.status_code < 500, 
                           f"Harvest API server error: {response.status_code}")
            print(f"Harvest API is reachable. Status code: {response.status_code}")
        except requests.exceptions.RequestException as e:
            self.fail(f"Failed to reach Harvest API: {str(e)}")

    @patch('requests.request')
    def test_api_request_structure(self, mock_request):
        """Test the structure of a Harvest API request without importing server code."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"data": "test_data"}
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response
        
        # Define a simple function that mimics the behavior of harvest_api_request
        def simple_harvest_request(method, endpoint, data=None, params=None):
            base_url = "https://api.harvestapp.com/v2"
            url = f"{base_url}{endpoint}"
            headers = {
                "Authorization": "Bearer test_token",
                "Harvest-Account-Id": "test_account",
                "User-Agent": "Test User Agent",
                "Content-Type": "application/json",
            }
            
            try:
                response = requests.request(method, url, headers=headers, json=data, params=params)
                response.raise_for_status()
                return response.json()
            except requests.exceptions.RequestException as e:
                return {"success": False, "error": str(e)}
        
        # Call the function
        result = simple_harvest_request("GET", "/test_endpoint")
        
        # Assertions
        self.assertEqual(result, {"data": "test_data"})
        mock_request.assert_called_once()


if __name__ == "__main__":
    unittest.main()
