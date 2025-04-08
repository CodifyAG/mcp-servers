"""
Pytest fixtures for testing Slack MCP server.
"""

import pytest
from unittest.mock import patch
from slack_sdk.web.slack_response import SlackResponse
from dotenv import load_dotenv

# Load environment variables from .env file for testing
load_dotenv()


@pytest.fixture
def mock_env_vars():
    """Fixture to mock environment variables."""
    with patch.dict(
        "os.environ", {"SLACK_BOT_TOKEN": "xoxb-test-token", "SLACK_TEAM_ID": "T12345"}
    ):
        yield


@pytest.fixture
def mock_slack_client():
    """Fixture for mocking the SlackClient."""
    with patch("slack_mcp.server.slack_client") as mock_client:
        # Set up common mocks
        mock_client.get_channels.return_value = {"ok": True, "channels": []}
        mock_client.post_message.return_value = {"ok": True, "ts": "1234567890.123456"}
        mock_client.post_reply.return_value = {"ok": True, "ts": "1234567891.123456"}
        mock_client.add_reaction.return_value = {"ok": True}
        mock_client.get_channel_history.return_value = {"ok": True, "messages": []}
        mock_client.get_thread_replies.return_value = {"ok": True, "messages": []}
        mock_client.get_users.return_value = {"ok": True, "members": []}
        mock_client._verify_auth.return_value = None

        yield mock_client


@pytest.fixture
def mock_web_client():
    """Fixture for mocking the Slack WebClient."""
    with patch("slack_sdk.web.WebClient") as mock_web_client:
        # Set up auth test response
        mock_instance = mock_web_client.return_value
        mock_instance.auth_test.return_value = {
            "ok": True,
            "user": "test-bot",
            "team": "test-team",
        }

        # Create mock response helper function
        def create_mock_response(
            data,
            http_verb="GET",
            api_url="test",
            req_args=None,
            headers=None,
            status_code=200,
        ):
            return SlackResponse(
                client=mock_instance,
                http_verb=http_verb,
                api_url=api_url,
                req_args=req_args or {},
                data=data,
                headers=headers or {},
                status_code=status_code,
            )

        # Add the helper to the mock for easy access
        mock_instance.create_mock_response = create_mock_response

        yield mock_instance


@pytest.fixture
def mock_fastmcp():
    """Fixture to mock FastMCP."""
    with patch("slack_mcp.server.FastMCP") as mock_fastmcp:
        mock_instance = mock_fastmcp.return_value
        yield mock_instance


@pytest.fixture
def sample_channel_data():
    """Sample channel data for testing."""
    return {
        "ok": True,
        "channels": [
            {
                "id": "C12345",
                "name": "general",
                "is_private": False,
                "is_archived": False,
                "created": 1503435957,
                "creator": "U12345",
            },
            {
                "id": "C67890",
                "name": "random",
                "is_private": False,
                "is_archived": False,
                "created": 1503435958,
                "creator": "U12345",
            },
        ],
    }


@pytest.fixture
def sample_users_data():
    """Sample users data for testing."""
    return {
        "ok": True,
        "members": [
            {
                "id": "U12345",
                "name": "user1",
                "real_name": "User One",
                "is_bot": False,
                "is_admin": True,
            },
            {
                "id": "U67890",
                "name": "user2",
                "real_name": "User Two",
                "is_bot": False,
                "is_admin": False,
            },
        ],
    }


@pytest.fixture
def sample_message_data():
    """Sample message data for testing."""
    return {
        "ok": True,
        "channel": "C12345",
        "ts": "1234567890.123456",
        "message": {
            "text": "Test message",
            "user": "U12345",
            "ts": "1234567890.123456",
        },
    }
