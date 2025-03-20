import pytest
from unittest.mock import MagicMock


@pytest.fixture
def mock_response():
    """Return a mock response object for testing."""
    mock = MagicMock()
    mock.json.return_value = {"data": "test_data"}
    mock.status_code = 200
    mock.raise_for_status.return_value = None
    return mock


@pytest.fixture
def mock_error_response():
    """Return a mock error response object for testing."""
    mock = MagicMock()
    mock.raise_for_status.side_effect = Exception("API Error")
    mock.status_code = 500
    return mock
