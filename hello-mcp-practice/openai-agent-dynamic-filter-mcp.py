import os
import asyncio
from dotenv import load_dotenv,find_dotenv
from agents import Agent,Runner, set_default_openai_api,set_default_openai_client,set_tracing_disabled
from openai import AsyncOpenAI
from agents.mcp import MCPServerStreamableHttp, MCPServerStreamableHttpParams, ToolFilterContext
_:bool = load_dotenv(find_dotenv())
MCP_SERVER_URL = "http://127.0.0.1:8000/mcp"

external_client = AsyncOpenAI(
    api_key=os.getenv("GOOGLE_API_KEY"),
    base_url=os.getenv("GOOGLE_BASE_URL")
)
set_default_openai_client(external_client)
set_default_openai_api("chat_completions")
set_tracing_disabled(True)

def dynamic_tool_filter(context: ToolFilterContext,tool) -> bool:
    print(f"Dynamic Tool Filter Invoked for tool: {tool.name} in context: {context}")
    if tool.name == "greeting_agent":
        return True
    if tool.name == "mood_agent":
        return False
    return True

async def main():
    mcp_params = MCPServerStreamableHttpParams(url=MCP_SERVER_URL)
    print("Using MCPServerStreamableHttp with URL:", mcp_params.get("url"))

    async with MCPServerStreamableHttp(params=mcp_params,name="MCPServerClient",cache_tools_list=True,tool_filter=dynamic_tool_filter) as mcp_server_client:
        print(f"MCP Server Client initialized {mcp_server_client.name}")
        print("Agent SDK Will Use This MCP Server Client For Interacting With The MCP Server")

        agent = Agent(
            name = "MCPServerAgent",
            instructions="An Assistant that uses the MCP server tools to greet users and respond to their mood.",
            mcp_servers=[mcp_server_client],
            model = "gemini-2.5-flash"
        )
        print(f"Agent initialized {agent.name} with MCP Server {mcp_server_client.name}")
        print("Agent Will Use This MCP Server Client For Interacting With The MCP Server")

        print(f"Agent Attempting to list tools from MCP Server {mcp_server_client.name}")
        tools = await mcp_server_client.list_tools(
            run_context = object(),
            agent = object()
        )
        print(f"Tools Found: {tools}")

        runner = await Runner.run(
            starting_agent=agent,
            input="Hello, My name is Sam , can you greet me."
        )

        print(f"Agent Response : {runner.final_output}")
    
    print(f"MCPServerStreamableHttp client '{mcp_server_client.name}' context exited.")

if __name__ == "__main__":
    asyncio.run(main())


    
