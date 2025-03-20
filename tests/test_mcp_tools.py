import unittest
from unittest.mock import patch, MagicMock
import requests


class TestMCPBasicFunctionality(unittest.TestCase):
    """Test basic functionality related to MCP tools."""

    def test_requests_library_available(self):
        """Test that the requests library is available and working."""
        self.assertTrue(hasattr(requests, 'get'))
        self.assertTrue(hasattr(requests, 'post'))
        self.assertTrue(hasattr(requests, 'patch'))
        self.assertTrue(hasattr(requests, 'delete'))
    
    @patch('requests.request')
    def test_basic_api_request_pattern(self, mock_request):
        """Test a basic API request pattern without importing server code."""
        # Setup mock response
        mock_response = MagicMock()
        mock_response.json.return_value = {"success": True}
        mock_response.raise_for_status.return_value = None
        mock_request.return_value = mock_response
        
        # Define a simple function that mimics a tool function
        def simple_tool_function(param1, param2=None):
            data = {"param1": param1}
            if param2:
                data["param2"] = param2
                
            response = requests.request(
                "POST", 
                "https://api.harvestapp.com/v2/endpoint",
                headers={"Content-Type": "application/json"},
                json=data
            )
            response.raise_for_status()
            return response.json()
        
        # Call the function
        result = simple_tool_function("test_value")
        
        # Assertions
        self.assertEqual(result, {"success": True})
        mock_request.assert_called_once()


if __name__ == "__main__":
    unittest.main()
