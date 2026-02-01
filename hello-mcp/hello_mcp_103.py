from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name="Hello MCP", stateless_http = True)

@mcp.tool(name="Research Tool",description="The Research Tool For Research Purpose")
def search_tool(query:str):
    return f"Research is being done on your {query}"

@mcp.tool(name="Info Tool",description="Information about the User")
def info(name:str,age:int):
    return f"Your name is {name} with your age {age}"

mcp_app = mcp.streamable_http_app()