# laundry-timer-mcp

This project implements an MCP (Model Context Protocol) server designed to help with laundry planning.

## How it works

The server provides tools to access information about laundry preferences and real-time weather forecasts. An AI
assistant can leverage these tools to determine the best times for washing and drying clothes, especially when
line-drying is the preferred method.

## Usage with Claude Desktop for Laundry Planning

When connected to an assistant like Claude Desktop, this MCP server allows for natural language queries about laundry
planning.

You’ll need to add this server in the mcpServers key.

```json
{
  "mcpServers": {
    "laundry-timer": {
      "command": "uv",
      "args": [
        "--directory",
        "/ABSOLUTE/PATH/TO/PARENT/FOLDER/laundry-timer-mcp",
        "run",
        "server.py"
      ]
    }
  }
}
```

After that, for example, you could ask: "Is it a good time to do my laundry today at Sydney, NSW?"

## Further Improvements

### Detailed Electricity Time-of-Use (TOU) Tariffs

To make the laundry planning even smarter, the server could be enhanced to include information about electricity
pricing. By integrating with a data source for Time-of-Use (TOU) tariffs, the assistant could identify periods of the
day when electricity is least expensive.

