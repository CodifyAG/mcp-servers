"""
Unit tests for the Slack client module.
"""

import pytest
from unittest.mock import patch
from slack_sdk.errors import SlackApiError
from slack_sdk.web.slack_response import SlackResponse

from slack_mcp.client import SlackClient


@pytest.fixture
def mock_slack_client():
    """Fixture for a mocked Slack client."""
    with patch("slack_mcp.client.WebClient") as mock_web_client:
        # Set up auth test response
        mock_instance = mock_web_client.return_value
        mock_instance.auth_test.return_value = {
            "ok": True,
            "user": "test-bot",
            "team": "test-team",
        }

        client = SlackClient("xoxb-test-token", "T12345")
        # Replace the actual WebClient with our mock
        client.client = mock_instance
        yield client


def test_get_channels(mock_slack_client):
    """Test getting channels."""
    # Setup mock response
    mock_channels = {
        "ok": True,
        "channels": [
            {"id": "C12345", "name": "general", "is_private": False},
            {"id": "C67890", "name": "random", "is_private": False},
        ],
    }
    mock_response = SlackResponse(
        client=mock_slack_client.client,
        http_verb="GET",
        api_url="conversations.list",
        req_args={},
        data=mock_channels,
        headers={},
        status_code=200,
    )
    mock_slack_client.client.conversations_list.return_value = mock_response

    # Call the method
    result = mock_slack_client.get_channels()

    # Verify results
    assert result == mock_channels
    mock_slack_client.client.conversations_list.assert_called_once_with(
        types="public_channel", exclude_archived=True, limit=100, cursor=None
    )


def test_get_channel_history(mock_slack_client):
    """Test fetching channel history."""
    mock_history = {
        "ok": True,
        "messages": [
            {
                "type": "message",
                "user": "U12345",
                "text": "Hello!",
                "ts": "1234567890.000100",
            },
            {
                "type": "message",
                "user": "U67890",
                "text": "Hi!",
                "ts": "1234567890.000200",
            },
        ],
    }
    mock_response = SlackResponse(
        client=mock_slack_client.client,
        http_verb="GET",
        api_url="conversations.history",
        req_args={},
        data=mock_history,
        headers={},
        status_code=200,
    )
    mock_slack_client.client.conversations_history.return_value = mock_response

    # Call the method
    result = mock_slack_client.get_channel_history("C12345", limit=2)

    # Verify results
    assert result == mock_history
    mock_slack_client.client.conversations_history.assert_called_once_with(
        channel="C12345", limit=2
    )


def test_post_message(mock_slack_client):
    """Test posting a message."""
    # Setup mock response
    mock_message = {
        "ok": True,
        "channel": "C12345",
        "ts": "1234567890.123456",
        "message": {"text": "Test message"},
    }
    mock_response = SlackResponse(
        client=mock_slack_client.client,
        http_verb="POST",
        api_url="chat.postMessage",
        req_args={},
        data=mock_message,
        headers={},
        status_code=200,
    )
    mock_slack_client.client.chat_postMessage.return_value = mock_response

    # Call the method
    result = mock_slack_client.post_message("C12345", "Test message")

    # Verify results
    assert result == mock_message
    mock_slack_client.client.chat_postMessage.assert_called_once_with(
        channel="C12345", text="Test message"
    )


def test_post_message_error(mock_slack_client):
    """Test posting a message with an error."""
    # Setup mock error
    mock_slack_client.client.chat_postMessage.side_effect = SlackApiError(
        "Error", {"error": "channel_not_found"}
    )

    # Call the method
    result = mock_slack_client.post_message("invalid-channel", "Test message")

    # Verify results
    assert result["ok"] is False
    assert "Error" in result["error"]


def test_post_reply(mock_slack_client):
    """Test posting a threaded reply."""
    mock_reply = {
        "ok": True,
        "channel": "C12345",
        "ts": "1234567890.123456",
        "message": {"text": "Thread reply"},
    }
    mock_response = SlackResponse(
        client=mock_slack_client.client,
        http_verb="POST",
        api_url="chat.postMessage",
        req_args={},
        data=mock_reply,
        headers={},
        status_code=200,
    )
    mock_slack_client.client.chat_postMessage.return_value = mock_response

    # Call the method
    result = mock_slack_client.post_reply("C12345", "1234567890.000000", "Thread reply")

    # Verify results
    assert result == mock_reply
    mock_slack_client.client.chat_postMessage.assert_called_once_with(
        channel="C12345", thread_ts="1234567890.000000", text="Thread reply"
    )


def test_get_users(mock_slack_client):
    """Test getting users list."""
    # Setup mock response
    mock_users = {
        "ok": True,
        "members": [
            {"id": "U12345", "name": "user1", "real_name": "User One"},
            {"id": "U67890", "name": "user2", "real_name": "User Two"},
        ],
    }
    mock_response = SlackResponse(
        client=mock_slack_client.client,
        http_verb="GET",
        api_url="users.list",
        req_args={},
        data=mock_users,
        headers={},
        status_code=200,
    )
    mock_slack_client.client.users_list.return_value = mock_response

    # Call the method
    result = mock_slack_client.get_users()

    # Verify results
    assert result == mock_users
    mock_slack_client.client.users_list.assert_called_once_with(limit=100, cursor=None)


def test_add_reaction(mock_slack_client):
    """Test adding a reaction."""
    # Setup mock response
    mock_reaction = {
        "ok": True,
    }
    mock_response = SlackResponse(
        client=mock_slack_client.client,
        http_verb="POST",
        api_url="reactions.add",
        req_args={},
        data=mock_reaction,
        headers={},
        status_code=200,
    )
    mock_slack_client.client.reactions_add.return_value = mock_response

    # Call the method
    result = mock_slack_client.add_reaction("C12345", "1234567890.123456", "thumbsup")

    # Verify results
    assert result == mock_reaction
    mock_slack_client.client.reactions_add.assert_called_once_with(
        channel="C12345", timestamp="1234567890.123456", name="thumbsup"
    )


def test_schedule_message(mock_slack_client):
    """Test scheduling a message."""
    mock_scheduled = {
        "ok": True,
        "scheduled_message_id": "Q12345678",
        "post_at": 1700000000,
        "channel": "C12345",
    }
    mock_response = SlackResponse(
        client=mock_slack_client.client,
        http_verb="POST",
        api_url="chat.scheduleMessage",
        req_args={},
        data=mock_scheduled,
        headers={},
        status_code=200,
    )
    mock_slack_client.client.chat_scheduleMessage.return_value = mock_response

    # Call the method
    result = mock_slack_client.schedule_message("C12345", "Scheduled text", 1700000000)

    # Verify results
    assert result == mock_scheduled
    mock_slack_client.client.chat_scheduleMessage.assert_called_once_with(
        channel="C12345", text="Scheduled text", post_at=1700000000
    )
