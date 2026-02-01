from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="Hello-MCP-Server", stateless_http=False)

@mcp.tool(name="weather_tool", description="A weather tool")
async def get_weather(city: str) -> str:
    return f"The weather in {city} is sunny with a temperature of 25°C."

mcp_app = mcp.streamable_http_app()