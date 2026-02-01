import os
import asyncio
from dotenv import load_dotenv,find_dotenv
from agents import Agent,Runner, set_default_openai_api,set_default_openai_client,set_tracing_disabled
from openai import AsyncOpenAI
from agents.mcp import MCPServerStreamableHttp, MCPServerStreamableHttpParams
_:bool = load_dotenv(find_dotenv())
MCP_SERVER_URL = "http://127.0.0.1:8000/mcp"

external_client = AsyncOpenAI(
    api_key=os.getenv("GOOGLE_API_KEY"),
    base_url=os.getenv("GOOGLE_BASE_URL")
)
set_default_openai_client(external_client)
set_default_openai_api("chat_completions")
set_tracing_disabled(True)

async def main():
    mcp_params = MCPServerStreamableHttpParams(url=MCP_SERVER_URL)
    print("Using MCPServerStreamableHttp with URL:", mcp_params.get("url"))

    async with MCPServerStreamableHttp(params=mcp_params,name="MCPServerClient", cache_tools_list=True) as mcp_server_client:
        print(f"MCP Server Client initialized {mcp_server_client.name}")
        print("Agent SDK Will Use This MCP Server Client For Interacting With The MCP Server")

        prompts = await mcp_server_client.list_prompts()
        print(f"Prompts Found: {prompts}")

        get_prompt = await mcp_server_client.get_prompt(
            name="greeting_prompt",
            arguments = {"user_name": "Sam"}
        )
        print(f"Prompt Retrieved: {get_prompt}")
        mcp_prompts = get_prompt.messages[0].content.text if get_prompt else "No prompt found"
        print(f"MCP Prompt Content: {mcp_prompts}")

        agent = Agent(
            name = "MCPServerAgent",
            instructions = mcp_prompts,
            mcp_servers=[mcp_server_client],
            model = "gemini-2.5-flash"
        )
        print(f"Agent initialized {agent.name} with MCP Server {mcp_server_client.name}")
        print("Agent Will Use This MCP Server Client For Interacting With The MCP Server")

        print(f"Agent Attempting to list tools from MCP Server {mcp_server_client.name}")
        tools = await mcp_server_client.list_tools()
        print(f"Tools Found: {tools}")

        runner = await Runner.run(
            starting_agent=agent,
            input="Hello, My name is Sam how are you ."
        )

        print(f"Agent Response : {runner.final_output}")
    
    print(f"MCPServerStreamableHttp client '{mcp_server_client.name}' context exited.")

if __name__ == "__main__":
    asyncio.run(main())


    
