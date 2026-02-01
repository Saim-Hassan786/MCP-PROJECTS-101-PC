from mcp.server.fastmcp import FastMCP

mcp = FastMCP(
    name = "MCPServerForAgent",
    stateless_http=True,
    json_response=True
)

@mcp.tool(
    name = "greeting_agent",
    description="A tool that greets the user",
)
def greeting_agent(name: str) -> str:
    print(f"Greeting {name} from MCPServer")
    return f"Hello, {name}! From MCPServerForAgent How can I assist you today?"

@mcp.tool(
    name = "mood_agent",
    description="A tool that tells the user's mood",
)
def mood_agent(mood: str) -> str:
    print(f"User's mood is {mood} from MCPServer")
    return f"I'm glad to hear you're feeling {mood}! From MCPServerForAgent How can I assist you today?"

@mcp.prompt(
    name="greeting_prompt",
    description="A prompt that greets the user",
)
def mcp_prompt(user_name: str):
    return f"You are a helpful assistant that provides help to the {user_name} in the best ways possible"


mcp_app = mcp.streamable_http_app()