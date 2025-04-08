"""
Slack API client for MCP server.
"""

from typing import Optional, Dict, Any
import logging
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError

logger = logging.getLogger(__name__)


class SlackClient:
    """Client for interacting with the Slack API."""

    def __init__(self, bot_token: str, team_id: str):
        """Initialize the Slack client.

        Args:
            bot_token: Slack bot token
            team_id: Slack team ID
        """
        self.client = WebClient(token=bot_token)
        self.team_id = team_id
        self._verify_auth()

    def _verify_auth(self) -> None:
        """Verify authentication with Slack."""
        try:
            auth_response = self.client.auth_test()
            logger.info(
                f"Connected to Slack as {auth_response['user']} in workspace {auth_response['team']}"
            )
        except SlackApiError as e:
            logger.error(f"Authentication failed: {e}")
            raise

    def get_channels(
        self,
        limit: int = 100,
        cursor: Optional[str] = None,
        types: str = "public_channel",
    ) -> Dict[str, Any]:
        """List public channels in the workspace.

        Args:
            limit: Maximum number of channels to return
            cursor: Pagination cursor for next page of results

        Returns:
            Slack API response
        """
        try:
            response = self.client.conversations_list(
                types=types,
                exclude_archived=True,
                limit=min(limit, 200),
                cursor=cursor,
            )
            return response.data
        except SlackApiError as e:
            logger.error(f"Error listing channels: {e}")
            return {"ok": False, "error": str(e)}

    def post_message(self, channel_id: str, text: str) -> Dict[str, Any]:
        """Post a message to a channel.

        Args:
            channel_id: Channel ID
            text: Message text

        Returns:
            Slack API response
        """
        try:
            response = self.client.chat_postMessage(channel=channel_id, text=text)
            return response.data
        except SlackApiError as e:
            logger.error(f"Error posting message: {e}")
            return {"ok": False, "error": str(e)}

    def schedule_message(
        self, channel_id: str, text: str, post_at: int
    ) -> Dict[str, Any]:
        """Schedule a message to be sent at a later time.

        Args:
            channel_id: Channel ID
            text: Message text
            post_at: Unix timestamp (in seconds) for when to send the message

        Returns:
            Slack API response
        """
        try:
            response = self.client.chat_scheduleMessage(
                channel=channel_id, text=text, post_at=post_at
            )
            return response.data
        except SlackApiError as e:
            logger.error(f"Error scheduling message: {e}")
            return {"ok": False, "error": str(e)}

    def post_reply(self, channel_id: str, thread_ts: str, text: str) -> Dict[str, Any]:
        """Post a reply to a thread.

        Args:
            channel_id: Channel ID
            thread_ts: Parent message timestamp
            text: Reply text

        Returns:
            Slack API response
        """
        try:
            response = self.client.chat_postMessage(
                channel=channel_id, thread_ts=thread_ts, text=text
            )
            return response.data
        except SlackApiError as e:
            logger.error(f"Error posting reply: {e}")
            return {"ok": False, "error": str(e)}

    def add_reaction(
        self, channel_id: str, timestamp: str, reaction: str
    ) -> Dict[str, Any]:
        """Add a reaction to a message.

        Args:
            channel_id: Channel ID
            timestamp: Message timestamp
            reaction: Emoji name

        Returns:
            Slack API response
        """
        try:
            response = self.client.reactions_add(
                channel=channel_id, timestamp=timestamp, name=reaction
            )
            return response.data
        except SlackApiError as e:
            logger.error(f"Error adding reaction: {e}")
            return {"ok": False, "error": str(e)}

    def list_scheduled_messages(
        self, channel_id: str, limit: int = 100, cursor: Optional[str] = None
    ) -> Dict[str, Any]:
        """List scheduled messages for a channel.

        Args:
            channel_id: Channel ID
            limit: Maximum number of scheduled messages to return
            cursor: Pagination cursor for next page of results

        Returns:
            Slack API response
        """
        try:
            response = self.client.chat_scheduledMessages_list(
                channel=channel_id, limit=min(limit, 1000), cursor=cursor
            )
            return response.data
        except SlackApiError as e:
            logger.error(f"Error listing scheduled messages: {e}")
            return {"ok": False, "error": str(e)}

    def delete_scheduled_message(
        self, channel_id: str, scheduled_message_id: str
    ) -> Dict[str, Any]:
        """Delete a scheduled message.

        Args:
            channel_id: Channel ID
            scheduled_message_id: ID of the scheduled message to delete

        Returns:
            Slack API response
        """
        try:
            response = self.client.chat_deleteScheduledMessage(
                channel=channel_id, scheduled_message_id=scheduled_message_id
            )
            return response.data
        except SlackApiError as e:
            logger.error(f"Error deleting scheduled message: {e}")
            return {"ok": False, "error": str(e)}

    def get_channel_history(self, channel_id: str, limit: int = 10) -> Dict[str, Any]:
        """Get recent messages from a channel.

        Args:
            channel_id: Channel ID
            limit: Number of messages to retrieve

        Returns:
            Slack API response
        """
        try:
            response = self.client.conversations_history(
                channel=channel_id, limit=limit
            )
            return response.data
        except SlackApiError as e:
            logger.error(f"Error getting channel history: {e}")
            return {"ok": False, "error": str(e)}

    def get_thread_replies(self, channel_id: str, thread_ts: str) -> Dict[str, Any]:
        """Get replies in a thread.

        Args:
            channel_id: Channel ID
            thread_ts: Parent message timestamp

        Returns:
            Slack API response
        """
        try:
            response = self.client.conversations_replies(
                channel=channel_id, ts=thread_ts
            )
            return response.data
        except SlackApiError as e:
            logger.error(f"Error getting thread replies: {e}")
            return {"ok": False, "error": str(e)}

    def get_users(
        self, limit: int = 100, cursor: Optional[str] = None
    ) -> Dict[str, Any]:
        """Get users in the workspace.

        Args:
            limit: Maximum number of users to return
            cursor: Pagination cursor for next page of results

        Returns:
            Slack API response
        """
        try:
            response = self.client.users_list(limit=min(limit, 200), cursor=cursor)
            return response.data
        except SlackApiError as e:
            logger.error(f"Error getting users: {e}")
            return {"ok": False, "error": str(e)}

    def get_user_profile(self, user_id: str) -> Dict[str, Any]:
        """Get detailed profile for a user.

        Args:
            user_id: User ID

        Returns:
            Slack API response
        """
        try:
            response = self.client.users_profile_get(user=user_id, include_labels=True)
            return response.data
        except SlackApiError as e:
            logger.error(f"Error getting user profile: {e}")
            return {"ok": False, "error": str(e)}
