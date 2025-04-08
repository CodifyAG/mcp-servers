"""
Slack MCP Server implementation.
"""

import os
import json
import logging
from dotenv import load_dotenv

from mcp.server.fastmcp import FastMCP

from slack_mcp.client import SlackClient

from slack_mcp.models import (
    GetChannelHistoryArgs,
    AddReactionArgs,
    GetUsersArgs,
    PostMessageArgs,
    ReplyToThreadArgs,
    ListChannelsArgs,
    DeleteScheduledMessageArgs,
    ListScheduledMessagesArgs,
    ScheduleMessageArgs,
)


# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_TEAM_ID = os.getenv("SLACK_TEAM_ID")

if not SLACK_BOT_TOKEN or not SLACK_TEAM_ID:
    raise EnvironmentError(
        "SLACK_BOT_TOKEN and SLACK_TEAM_ID environment variables are required"
    )

# Initialize MCP server
mcp = FastMCP("Slack MCP Server")

# Initialize Slack client
slack_client = SlackClient(SLACK_BOT_TOKEN, SLACK_TEAM_ID)


# Tool implementations
@mcp.tool()
async def slack_list_channels(args: ListChannelsArgs) -> str:
    """List public and private channels the bot can access with pagination.

    Args:
        limit: Number of channels to retrieve per call.
        cursor: Cursor for pagination.

    Returns:
        JSON string containing channels data.
    """
    logger.info(f"Listing channels with args: limit={args.limit}, cursor={args.cursor}")
    response = slack_client.get_channels(
        limit=args.limit, cursor=args.cursor, types="public_channel,private_channel"
    )
    return json.dumps(response)


@mcp.tool()
async def slack_post_message(args: PostMessageArgs) -> str:
    """Post a new message to a Slack channel.

    Args:
        args: Tool arguments (channel_id, text)

    Returns:
        JSON string containing message post result
    """
    logger.info(f"Posting message to channel {args.channel_id}")
    response = slack_client.post_message(args.channel_id, args.text)
    return json.dumps(response)


@mcp.tool()
async def slack_reply_to_thread(args: ReplyToThreadArgs) -> str:
    """Reply to a specific message thread in Slack.

    Args:
        args: Tool arguments (channel_id, thread_ts, text)

    Returns:
        JSON string containing reply result
    """
    logger.info(f"Replying to thread in channel {args.channel_id}")
    response = slack_client.post_reply(args.channel_id, args.thread_ts, args.text)
    return json.dumps(response)


@mcp.tool()
async def slack_add_reaction(args: AddReactionArgs) -> str:
    """Add a reaction emoji to a message.

    Args:
        args: Tool arguments (channel_id, timestamp, reaction)

    Returns:
        JSON string containing reaction result
    """
    logger.info(f"Adding reaction {args.reaction} to message in {args.channel_id}")
    response = slack_client.add_reaction(args.channel_id, args.timestamp, args.reaction)
    return json.dumps(response)


@mcp.tool()
async def slack_get_channel_history(args: GetChannelHistoryArgs) -> str:
    """Get recent messages from a channel.

    Args:
        args: Tool arguments (channel_id, limit)

    Returns:
        JSON string containing channel history
    """
    response = slack_client.get_channel_history(args.channel_id, limit=args.limit)
    return json.dumps(response)


@mcp.tool()
async def slack_get_thread_replies(channel_id: str, thread_ts: str) -> str:
    """Get all replies in a message thread.

    Args:
        args: Tool arguments (channel_id, thread_ts)

    Returns:
        JSON string containing thread replies
    """
    logger.info(f"Getting thread replies in {channel_id}")
    response = slack_client.get_thread_replies(channel_id, thread_ts)
    return json.dumps(response)


@mcp.tool()
async def slack_get_users(args: GetUsersArgs) -> str:
    """Get a list of all users in the workspace with their basic profile information.

    Args:
        args: Tool arguments (limit, cursor)

    Returns:
        JSON string containing users data
    """
    logger.info("Getting users list")
    response = slack_client.get_users(limit=args.limit, cursor=args.cursor)
    return json.dumps(response)


@mcp.tool()
async def schedule_message(args: ScheduleMessageArgs) -> str:
    """Schedule a message to be sent at a specific time.

    Args:
        args: Tool arguments (channel_id, text, post_at)

    Returns:
        JSON string containing schedule result
    """
    logger.info(f"Scheduling message in {args.channel_id} at {args.post_at}")
    response = slack_client.schedule_message(args.channel_id, args.text, args.post_at)
    return json.dumps(response)


@mcp.tool()
async def list_scheduled_messages(args: ListScheduledMessagesArgs) -> str:
    """List scheduled messages in a channel.

    Args:
        args: Tool arguments (channel_id, limit, cursor)

    Returns:
        JSON string containing scheduled messages
    """
    logger.info(f"Listing scheduled messages in {args.channel_id}")
    response = slack_client.list_scheduled_messages(
        args.channel_id, limit=args.limit, cursor=args.cursor
    )
    return json.dumps(response)


@mcp.tool()
async def delete_scheduled_message(args: DeleteScheduledMessageArgs) -> str:
    """Delete a scheduled message.

    Args:
        args: Tool arguments (channel_id, scheduled_message_id)

    Returns:
        JSON string containing delete result
    """
    logger.info(
        f"Deleting scheduled message {args.scheduled_message_id} in {args.channel_id}"
    )
    response = slack_client.delete_scheduled_message(
        args.channel_id, args.scheduled_message_id
    )
    return json.dumps(response)


def main():
    """Main entry point for the server."""
    logger.info("Starting Slack MCP Server...")
    try:
        # Verify connection to Slack
        slack_client._verify_auth()

        # Run the server
        mcp.run()
    except Exception as e:
        logger.error(f"Error starting server: {e}", exc_info=True)
        exit(1)


if __name__ == "__main__":
    main()
