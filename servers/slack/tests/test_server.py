"""
Unit tests for the Slack MCP server.
"""

import json
import pytest
from unittest.mock import patch

from servers.slack.slack_mcp.models import (
    GetUsersArgs,
    PostMessageArgs,
    ReplyToThreadArgs,
)
from slack_mcp.server import ListChannelsArgs


# Import the server module
from slack_mcp.server import (
    slack_list_channels,
    slack_post_message,
    slack_reply_to_thread,
)


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

        yield mock_client


@pytest.mark.asyncio
async def test_slack_list_channels(mock_slack_client):
    """Test the slack_list_channels tool."""
    # Set up test data
    mock_channels = {
        "ok": True,
        "channels": [
            {"id": "C12345", "name": "general"},
            {"id": "C67890", "name": "random"},
        ],
    }
    mock_slack_client.get_channels.return_value = mock_channels

    args = ListChannelsArgs(limit=50, cursor=None)

    # Call the tool function
    result = await slack_list_channels(args)

    # Verify the result
    assert isinstance(result, str)
    parsed_result = json.loads(result)
    assert parsed_result == mock_channels

    # Verify the client was called correctly

    mock_slack_client.get_channels.assert_called_once_with(
        limit=50, cursor=None, types="public_channel,private_channel"
    )


@pytest.mark.asyncio
async def test_slack_post_message(mock_slack_client):
    """Test the slack_post_message tool."""
    # Set up test data
    mock_response = {
        "ok": True,
        "channel": "C12345",
        "ts": "1234567890.123456",
        "message": {"text": "Test message"},
    }
    mock_slack_client.post_message.return_value = mock_response

    args = PostMessageArgs(channel_id="C12345", text="Test message")
    # Call the tool function
    result = await slack_post_message(args)

    # Verify the result
    assert isinstance(result, str)
    parsed_result = json.loads(result)
    assert parsed_result == mock_response

    # Verify the client was called correctly
    mock_slack_client.post_message.assert_called_once_with("C12345", "Test message")


@pytest.mark.asyncio
async def test_slack_reply_to_thread(mock_slack_client):
    """Test the slack_reply_to_thread tool."""
    # Set up test data
    mock_response = {
        "ok": True,
        "channel": "C12345",
        "ts": "1234567891.123456",
        "message": {"text": "Test reply"},
    }
    mock_slack_client.post_reply.return_value = mock_response

    args = ReplyToThreadArgs(
        channel_id="C12345", thread_ts="1234567890.123456", text="Test reply"
    )
    # Call the tool function
    result = await slack_reply_to_thread(args)

    # Verify the result
    assert isinstance(result, str)
    parsed_result = json.loads(result)
    assert parsed_result == mock_response

    # Verify the client was called correctly
    mock_slack_client.post_reply.assert_called_once_with(
        "C12345", "1234567890.123456", "Test reply"
    )


@pytest.mark.asyncio
async def test_slack_get_users(mock_slack_client):
    """Test the slack_get_users tool."""
    # Set up test data
    mock_users = {
        "ok": True,
        "members": [
            {"id": "U12345", "name": "user1", "real_name": "User One"},
            {"id": "U67890", "name": "user2", "real_name": "User Two"},
        ],
    }
    mock_slack_client.get_users.return_value = mock_users

    # For this test, we need to directly import the tool function
    from slack_mcp.server import slack_get_users

    args = GetUsersArgs(limit=10)
    # Call the tool function
    result = await slack_get_users(args)

    # Verify the result
    assert isinstance(result, str)
    parsed_result = json.loads(result)
    assert parsed_result == mock_users

    # Verify the client was called correctly
    mock_slack_client.get_users.assert_called_once_with(limit=10, cursor=None)
