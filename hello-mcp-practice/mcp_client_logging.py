import asyncio
from mcp.client.streamable_http import streamablehttp_client
from mcp.client.session import ClientSession
from mcp.types import LoggingMessageNotificationParams

async def logging_handler(params: LoggingMessageNotificationParams):
    emoji_map = {
        "debug": "🔍",
        "info": "📰",
        "warning": "⚠️",
        "error": "❌",
    }
    emoji = emoji_map.get(params.level.lower(), "📝")
    logger_info = f" [{params.logger}]" if params.logger else ""
    print(f"    {emoji} [{params.level.upper()}]{logger_info} {params.data}")

async def main():
    url = "http://localhost:8000/mcp/"
    print("Connecting to MCP server...")

    async with streamablehttp_client(url) as (read_stream, write_stream, session_id):
        async with ClientSession(read_stream, write_stream,logging_callback=logging_handler) as session:
            await session.initialize()
            print("Session initialized")
            
            print(f"Scenario 1")
            item_id = 42
            should_fail = False
            result = await session.call_tool(
                "log_event",
                {"item_id": item_id, "should_fail": should_fail}
            )
            print("-" * 50)
            print(f"Result: {result.content[0].text}")


            print(f"\nScenario 2")
            item_id = 99
            should_fail = True
            result = await session.call_tool(
                "log_event",
                {"item_id": item_id, "should_fail": should_fail}
            )
            print("-" * 50)
            print(f"Result: {result.content[0].text}")


if __name__ == "__main__":
    asyncio.run(main())

