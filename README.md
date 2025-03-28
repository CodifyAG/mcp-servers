# MCP Servers

A central repository for multiple [Model Context Protocol (MCP)](https://modelcontextprotocol.io/) server implementations. This repository contains various MCP servers that enable seamless integration with different services through the Model Context Protocol.

## Available Servers

| Server | Description | Status |
|--------|-------------|--------|
| [Harvest](/servers/harvest) | Time tracking and project management | ✅ Active |
| Binance | Cryptocurrency exchange API | 🚧 Planned |

## Repository Structure

```
mcp-servers/
├── servers/                  # Directory containing all MCP servers
│   ├── harvest/              # Harvest Time Tracking MCP server
│   │   ├── src/              # Server implementation
│   │   ├── tests/            # Server tests
│   │   └── README.md         # Server documentation
│   └── binance/              # Binance MCP server (planned)
└── examples/                 # Example usage for all servers
```

## Getting Started

Each server has its own documentation and setup instructions. Please refer to the specific server's README for details:

- [Harvest MCP Server](/servers/harvest)
- Binance MCP Server (Coming soon)

## Contributing

Please see [CONTRIBUTING.md](CONTRIBUTING.md) for details on how to contribute to this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
