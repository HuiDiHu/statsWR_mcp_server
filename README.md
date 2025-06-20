statsWR mcp server


setup:
1) source .venv/bin/activate
2) make setup

windows setup (additional steps on https://modelcontextprotocol.io/quickstart/server#windows): 
1) uv venv
2) source .venv/Scripts/activate
3) uv add mcp[cli] httpx
4) code $env:AppData\Claude\claude_desktop_config.json (follow directions in link)
5) pip install .
6) (may need to open task manager and manually terminate claude before opening it again for the MCP server to show up)