import asyncio
from typing import Any

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from mcp.types import CreateMessageResult,CreateMessageRequestParams,TextContent
from mcp.shared.context import RequestContext

async def mock_llm_reply(context:RequestContext["ClientSession",Any],params:CreateMessageRequestParams)->CreateMessageResult:
    print(f"Server Called The Client For Its LLM")
    print(f"Params: {params}")
    print(f"Context: {context}")
    print(f"Messages:{params.messages}")

    llm_mock_reply = (
        f"My name is Saim Hassan. "
        f"I am a student of PIAIC. "
        f"I am currently studying Agentic AI."
    )

    return CreateMessageResult(
        role = "assistant",
        content= TextContent(
            type="text",
            text=llm_mock_reply
        ),
        model="gemini-2.5-flash"
    )
async def main():
    url = "http://localhost:8000/mcp/"
    print("Connecting to MCP server...")

    async with streamablehttp_client(url) as (read_stream, write_stream, session_id):
        async with ClientSession(read_stream, write_stream,sampling_callback=mock_llm_reply) as session:
            await session.initialize()
            print("Session initialized")

            story_topic = "Artificial Intelligence And Saim Hassan"
            print(f"Creating story about: {story_topic}")
            print("Calling create_story tool...")
            tool_result = await session.call_tool(
                "create_story",
                {"topic": story_topic}
            )
            print("-" * 50)
            print(f"🎉 Final Story Received from Server: {tool_result}")
            if tool_result:
                print(f"'{tool_result.content[0].text}'")
            else:
                print("No content received from server.")

            print("\n✅ Demo complete!")

if __name__ == "__main__":
    asyncio.run(main())