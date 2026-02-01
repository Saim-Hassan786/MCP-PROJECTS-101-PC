from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="Hello MCP",stateless_http = True)

mcp_app = mcp.streamable_http_app()
