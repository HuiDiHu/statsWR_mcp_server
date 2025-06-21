# statsWR mcp server

**Windows Setup:** (additional steps on https://modelcontextprotocol.io/quickstart/server#windows)
1) uv venv
2) source .venv/Scripts/activate
3) make setup
4) update claude_desktop_config.json: 
```
{
  "mcpServers": {
    "statsWR": {
      "command": "/Path/to/uv",
      "args": [
        "--directory",
        "/Path/to/Project/Root/Directory",
        "run",
        "src/statsWR_mcp_server.py"
      ]
    }
  }
}
```
5) create and setup .env file in the project's root directory
```
STATSWR_API_BASE_URL = <STATSWR OFFICIAL API BASE URL>/api/v1
DEFAULT_TIMEOUT = 60
...
```

**Local Testing:**
1) restart cluade desktop
2) enable statsWR MCP server in the model setting
3) interact with the model and verify MCP server is being used