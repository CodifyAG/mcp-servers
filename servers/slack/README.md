# Slack MCP Server

A Model Context Protocol (MCP) server for integrating AI assistants like Claude with Slack workspaces.

## Features

- List channels and users
- Send messages and thread replies
- Add reactions to messages
- Get channel history and thread replies
- Get user profiles

## Setup

1. Create a Slack app with the following permissions:

   - `channels:history`
   - `channels:read`
   - `chat:write`
   - `reactions:write`
   - `users:read`
   - `users:read.email`

2. Install the app to your workspace and get the Bot Token and Team ID

3. Set up environment variables:

SLACK_BOT_TOKEN=xoxb-your-token-here
SLACK_TEAM_ID=T012345678

4. Install the server:

```bash
uv init
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
uv add -e .
```

5. Run the server
   python -m slack_mcp

6. Using with Claude for Desktop

```json
{
  "mcpServers": {
    "slack": {
      "command": "python",
      "args": ["-m", "slack_mcp"],
      "env": {
        "SLACK_BOT_TOKEN": "xoxb-your-token-here",
        "SLACK_TEAM_ID": "T012345678"
      }
    }
  }
}
```
