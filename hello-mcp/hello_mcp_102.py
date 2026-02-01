from mcp.server.fastmcp import FastMCP

mcp = FastMCP(name = "Hello MCP 2", stateless_http = True)

@mcp.tool()
def search_query(query:str):
    return f"Searching For {query}"

@mcp.tool()
def info(name :str , age:int):
    return f"Name is {name} and Age is {age}"


mcp_app = mcp.streamable_http_app()