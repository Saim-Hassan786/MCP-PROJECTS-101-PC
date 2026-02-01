from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    name = "Hello-MCP-Server",
    stateless_http = True
)

@mcp.tool(name="greeting_tool",description="A greeting specialist tool")
def greet_user(name:str):
    return f"Good Morning {name}"

@mcp.tool(name = "addition_tool",description="An Addition specialist tool")
def addition(a:int,b:int):
    return f"The result is {a+b}"

@mcp.tool(name="user_info_tool",description="A UserInfo Specialist")
def user_info(name:str,age:int):
    return f"Name Of the User Is {name} and Age is {age} 🎊"

mcp_app = mcp.streamable_http_app()
