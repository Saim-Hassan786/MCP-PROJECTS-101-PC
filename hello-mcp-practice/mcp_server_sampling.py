from mcp.server.fastmcp import FastMCP,Context
from mcp.types import SamplingMessage, TextContent

mcp = FastMCP(name="Hello-MCP-Server", stateless_http=False)

@mcp.tool(name = "create_story", description = "Create a story based on a prompt")
async def create_story(ctx: Context,topic:str) -> str:
    print(f"Server Tool Called :, Topic: {topic}")
    try :
        print(f"Server Delegating Task Back To Client LLM")
        result = await ctx.session.create_message(
            messages=[
                SamplingMessage(
                    role="user",
                    content = TextContent(
                        type="text",
                        text=f"Create a story about {topic}."
                    )
                )],
            max_tokens=100,
            temperature=0.7
    )
        print(f"Server Received Result: {result}")
        return result.content.text

    except Exception as e:
        print(f"Error in create_story: {e}")
        return "An error occurred while creating the story."
    
mcp_app = mcp.streamable_http_app()