"""
Integration tests for the Slack MCP server.

These tests verify the MCP server's interaction with the Slack API
using a real Slack SDK but mocked API responses.
"""
import json
import pytest
import asyncio
from unittest.mock import patch, MagicMock

from slack_mcp.client import SlackClient
from slack_mcp.server import mcp


@pytest.fixture
def mock_slack_api():
    """Fixture to mock Slack API responses."""
    with patch('slack_sdk.web.WebClient.api_call') as mock_api_call:
        # Set up default responses for common methods
        def mock_api(*args, **kwargs):
            """Mock response based on method name."""
            method = kwargs.get('http_verb', '') + ' ' + kwargs.get('api_url', '')
            
            if 'auth.test' in method:
                return {"ok": True, "user": "test-bot", "team": "Test Team"}
                
            elif 'conversations.list' in method:
                return {
                    "ok": True,
                    "channels": [
                        {"id": "C12345", "name": "general", "is_private": False},
                        {"id": "C67890", "name": "random", "is_private": False}
                    ]
                }
                
            elif 'chat.postMessage' in method:
                return {
                    "ok": True,
                    "channel": kwargs.get('params', {}).get('channel', ''),
                    "ts": "1234567890.123456",
                    "message": {"text": kwargs.get('params', {}).get('text', '')}
                }
                
            elif 'users.list' in method:
                return {
                    "ok": True,
                    "members": [
                        {"id": "U12345", "name": "user1", "real_name": "User One"},
                        {"id": "U67890", "name": "user2", "real_name": "User Two"}
                    ]
                }
                
            # Default fallback
            return {"ok": True}
            
        mock_api_call.side_effect = mock_api
        yield mock_api_call


@pytest.fixture
def slack_client():
    """Fixture for creating a Slack client with mocked API."""
    with patch('slack_sdk.web.WebClient.api_call') as mock_api_call:
        # Mock auth.test response
        mock_api_call.return_value = {"ok": True, "user": "test-bot", "team": "Test Team"}
        
        # Create client with test token
        client = SlackClient("xoxb-test-token", "T12345")
        yield client


def test_server_initialization():
    """Test that the MCP server initializes correctly."""
    assert mcp is not None
    assert mcp._name == "Slack MCP Server"


@pytest.mark.asyncio
async def test_list_channels_integration(monkeypatch):
    """Test the list_channels tool with mocked client."""
    # Mock the Slack client's get_channels method
    mock_response = {
        "ok": True,
        "channels": [
            {"id": "C12345", "name": "general"},
            {"id": "C67890", "name": "random"}
        ]
    }
    
    # Create a mock for the client
    mock_client = MagicMock()
    mock_client.get_channels.return_value = mock_response
    
    # Replace the server's client with our mock
    from slack_mcp.server import slack_client
    monkeypatch.setattr('slack_mcp.server.slack_client', mock_client)
    
    # Call the server function
    from slack_mcp.server import slack_list_channels
    result = await slack_list_channels(limit=10)
    
    # Check the result
    assert isinstance(result, str)
    parsed = json.loads(result)
    assert parsed == mock_response
    
    # Verify the mock was called correctly
    mock_client.get_channels.assert_called_once_with(
        limit=10, cursor=None, types="public_channel,private_channel"
    )


@pytest.mark.asyncio
async def test_post_message_integration(monkeypatch):
    """Test the post_message tool with mocked client."""
    # Mock response
    mock_response = {
        "ok": True,
        "channel": "C12345",
        "ts": "1234567890.123456",
        "message": {"text": "Test message"}
    }
    
    # Create a mock for the client
    mock_client = MagicMock()
    mock_client.post_message.return_value = mock_response
    
    # Replace the server's client with our mock
    monkeypatch.setattr('slack_mcp.server.slack_client', mock_client)
    
    # Call the server function
    from slack_mcp.server import slack_post_message
    result = await slack_post_message(channel_id="C12345", text="Test message")
    
    # Check the result
    assert isinstance(result, str)
    parsed = json.loads(result)
    assert parsed == mock_response
    
    # Verify the mock was called correctly
    mock_client.post_message.assert_called_once_with("C12345", "Test message")


@pytest.mark.asyncio
async def test_get_users_integration(monkeypatch):
    """Test the get_users tool with mocked client."""
    # Mock response
    mock_response = {
        "ok": True,
        "members": [
            {"id": "U12345", "name": "user1", "real_name": "User One"},
            {"id": "U67890", "name": "user2", "real_name": "User Two"}
        ]
    }
    
    # Create a mock for the client
    mock_client = MagicMock()
    mock_client.get_users.return_value = mock_response
    
    # Replace the server's client with our mock
    monkeypatch.setattr('slack_mcp.server.slack_client', mock_client)
    
    # Call the server function
    from slack_mcp.server import slack_get_users
    result = await slack_get_users(limit=10)
    
    # Check the result
    assert isinstance(result, str)
    parsed = json.loads(result)
    assert parsed == mock_response
    
    # Verify the mock was called correctly
    mock_client.get_users.assert_called_once_with(limit=10, cursor=None)
