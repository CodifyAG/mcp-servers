"""
Pydantic models for Slack API data structures.
"""

from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator


class SlackUser(BaseModel):
    """Model for a Slack user."""

    id: str = Field(..., description="User ID")
    name: str = Field(..., description="User name")
    real_name: Optional[str] = Field(None, description="User's real name")
    is_bot: bool = Field(False, description="Whether the user is a bot")
    is_admin: Optional[bool] = Field(None, description="Whether the user is an admin")
    profile: Optional[Dict[str, Any]] = Field(None, description="User profile data")

    @field_validator("id")
    @classmethod
    def validate_user_id(cls, v):
        if not v.startswith("U"):
            raise ValueError("User ID must start with 'U'")
        return v


class SlackChannel(BaseModel):
    """Model for a Slack channel."""

    id: str = Field(..., description="Channel ID")
    name: str = Field(..., description="Channel name")
    is_private: bool = Field(False, description="Whether channel is private")
    is_archived: Optional[bool] = Field(
        False, description="Whether channel is archived"
    )
    created: Optional[int] = Field(None, description="Channel creation timestamp")
    creator: Optional[str] = Field(None, description="User ID of channel creator")
    topic: Optional[Dict[str, Any]] = Field(None, description="Channel topic")
    purpose: Optional[Dict[str, Any]] = Field(None, description="Channel purpose")

    @field_validator("id")
    @classmethod
    def validate_channel_id(cls, v):
        if not v.startswith("C"):
            raise ValueError("Channel ID must start with 'C'")
        return v


class SlackMessage(BaseModel):
    """Model for a Slack message."""

    channel_id: str = Field(..., description="Channel ID")
    ts: str = Field(..., description="Message timestamp")
    text: str = Field(..., description="Message text")
    user: Optional[str] = Field(None, description="User ID who sent the message")
    bot_id: Optional[str] = Field(None, description="Bot ID who sent the message")
    thread_ts: Optional[str] = Field(
        None, description="Parent thread timestamp if in thread"
    )
    reply_count: Optional[int] = Field(None, description="Number of replies in thread")
    reactions: Optional[List[Dict[str, Any]]] = Field(
        None, description="Message reactions"
    )

    @field_validator("user", "bot_id", mode="before")
    @classmethod
    def either_user_or_bot(cls, v, info):
        values = info.data
        if v is None and values.get("user") is None and values.get("bot_id") is None:
            raise ValueError("Either user or bot_id must be present")
        return v


class SlackReaction(BaseModel):
    """Model for a Slack reaction."""

    name: str = Field(..., description="Reaction emoji name")
    count: int = Field(..., description="Number of users who reacted")
    users: List[str] = Field(..., description="List of user IDs who reacted")


class SlackScheduledMessage(BaseModel):
    """Model for a scheduled Slack message."""

    id: str = Field(..., description="Scheduled message ID")
    channel_id: str = Field(..., description="Channel ID")
    post_at: int = Field(..., description="Unix timestamp when message will be sent")
    text: str = Field(..., description="Message text")

    @field_validator("id")
    @classmethod
    def validate_scheduled_message_id(cls, v):
        if not v.startswith("Q"):
            raise ValueError("Scheduled message ID must start with 'Q'")
        return v


class SlackApiResponse(BaseModel):
    """Generic Slack API response model."""

    ok: bool = Field(..., description="Whether the request was successful")
    error: Optional[str] = Field(None, description="Error message if request failed")

    # For pagination
    response_metadata: Optional[Dict[str, Any]] = Field(
        None, description="Response metadata"
    )


class ChannelsListResponse(SlackApiResponse):
    """Response model for listing channels."""

    channels: Optional[List[SlackChannel]] = Field(None, description="List of channels")


class UsersListResponse(SlackApiResponse):
    """Response model for listing users."""

    members: Optional[List[SlackUser]] = Field(None, description="List of users")


class MessageResponse(SlackApiResponse):
    """Response model for sending messages."""

    ts: Optional[str] = Field(None, description="Timestamp of the sent message")
    channel: Optional[str] = Field(None, description="Channel ID message was sent to")
    message: Optional[Dict[str, Any]] = Field(None, description="Message data")


class HistoryResponse(SlackApiResponse):
    """Response model for channel history."""

    messages: Optional[List[SlackMessage]] = Field(None, description="List of messages")
    has_more: Optional[bool] = Field(
        None, description="Whether there are more messages"
    )


class ScheduledMessageResponse(SlackApiResponse):
    """Response model for scheduled message operations."""

    scheduled_message_id: Optional[str] = Field(
        None, description="ID of the scheduled message"
    )
    post_at: Optional[int] = Field(
        None, description="When the message is scheduled for"
    )
    channel: Optional[str] = Field(None, description="Channel ID")


class ScheduledMessagesListResponse(SlackApiResponse):
    """Response model for listing scheduled messages."""

    scheduled_messages: Optional[List[SlackScheduledMessage]] = Field(
        None, description="List of scheduled messages"
    )


class ListChannelsArgs(BaseModel):
    """Arguments for listing channels."""

    limit: Optional[int] = Field(
        100, description="Maximum number of channels to return (default 100, max 200)"
    )
    cursor: Optional[str] = Field(
        None, description="Pagination cursor for next page of results"
    )


class PostMessageArgs(BaseModel):
    """Arguments for posting a message."""

    channel_id: str = Field(..., description="The ID of the channel to post to")
    text: str = Field(..., description="The message text to post")


class ReplyToThreadArgs(BaseModel):
    """Arguments for replying to a thread."""

    channel_id: str = Field(
        ..., description="The ID of the channel containing the thread"
    )
    thread_ts: str = Field(
        ...,
        description="The timestamp of the parent message in the format '1234567890.123456'. Timestamps in the format without the period can be converted by adding the period such that 6 numbers come after it.",
    )
    text: str = Field(..., description="The reply text")


class AddReactionArgs(BaseModel):
    """Arguments for adding a reaction."""

    channel_id: str = Field(
        ..., description="The ID of the channel containing the message"
    )
    timestamp: str = Field(..., description="The timestamp of the message to react to")
    reaction: str = Field(
        ..., description="The name of the emoji reaction (without ::)"
    )


class GetChannelHistoryArgs(BaseModel):
    """Arguments for getting channel history."""

    channel_id: str = Field(..., description="The ID of the channel")
    limit: Optional[int] = Field(
        10, description="Number of messages to retrieve (default 10)"
    )


class GetThreadRepliesArgs(BaseModel):
    """Arguments for getting thread replies."""

    channel_id: str = Field(
        ..., description="The ID of the channel containing the thread"
    )
    thread_ts: str = Field(
        ...,
        description="The timestamp of the parent message in the format '1234567890.123456'. Timestamps in the format without the period can be converted by adding the period such that 6 numbers come after it.",
    )


class GetUsersArgs(BaseModel):
    """Arguments for getting users."""

    limit: Optional[int] = Field(
        100, description="Maximum number of users to return (default 100, max 200)"
    )
    cursor: Optional[str] = Field(
        None, description="Pagination cursor for next page of results"
    )


class GetUserProfileArgs(BaseModel):
    """Arguments for getting a user profile."""

    user_id: str = Field(..., description="The ID of the user")


class ScheduleMessageArgs(BaseModel):
    """Arguments for scheduling a message."""

    channel_id: str = Field(..., description="The ID of the channel to post to")
    text: str = Field(..., description="The message text to post")
    post_at: str = Field(
        ..., description="The Unix timestamp for when to post the message"
    )


class ListScheduledMessagesArgs(BaseModel):
    """Arguments for listing scheduled messages."""

    channel_id: str = Field(..., description="The ID of the channel")
    limit: Optional[int] = Field(
        100, description="Maximum number of messages to return (default 100)"
    )
    cursor: Optional[str] = Field(
        None, description="Pagination cursor for next page of results"
    )


class DeleteScheduledMessageArgs(BaseModel):
    """Arguments for deleting a scheduled message."""

    channel_id: str = Field(
        ..., description="The ID of the channel containing the scheduled message"
    )
    scheduled_message_id: str = Field(
        ..., description="The ID of the scheduled message to delete"
    )


# Configuration models
class SlackConfig(BaseModel):
    """Configuration for the Slack MCP server."""

    bot_token: str = Field(..., description="Slack bot token")
    team_id: str = Field(..., description="Slack team ID")
    cache_ttl: int = Field(300, description="Cache TTL in seconds")
    max_retries: int = Field(3, description="Maximum number of retries for API calls")

    @field_validator("bot_token")
    @classmethod
    def validate_bot_token(cls, v):
        if not v.startswith("xoxb-"):
            raise ValueError("Bot token must start with 'xoxb-'")
        return v
