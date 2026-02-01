import asyncio
from mcp.client.streamable_http import streamablehttp_client
from mcp.client.session import ClientSession

async def progress_handler(progress:float, total:float, message:str):
    if total:
        percentage = (progress / total) * 100
        progress_bar = "█" * int(percentage // 5) + "░" * (20 - int(percentage // 5))
        print(f"    📊 [{progress_bar}] {percentage:.1f}% - {message or 'Working...'}")
    else:
        print(f"    📊 Progress: {progress} - {message or 'Working...'}")

async def main():
    url = "http://localhost:8000/mcp/"
    print("Connecting to MCP server...")

    async with streamablehttp_client(url) as (read_stream, write_stream, session_id):
        async with ClientSession(read_stream, write_stream) as session:
            init_session = await session.initialize()
            print(init_session.capabilities)
            tool_names = await session.list_tools()
            print(f"Available tools: {[tool.name for tool in tool_names.tools]}")

            scenarios = [
                {
                    "name": "long_task",
                    "args": {"file_name": "large_file.dat", "mb_size": 5}
                },
                {
                    "name": "process_data",
                    "args": {"data": 20}
                }
            ]
            for scenario in scenarios:
                print(f"\nScenario: {scenario['name']}")
                result = await session.call_tool(
                    scenario['name'],
                    scenario['args'],
                    progress_callback=progress_handler
                )
                print("-" * 50)
                if result.content:
                    print(f"Result: {result.content}")
                else:
                    print("Tool Call Completed ✨ (no content returned)")

    print("🎉 Demo completed!")
    print("\n💡 Progress updates were sent in real-time via MCP protocol!")

if __name__ == "__main__":
    asyncio.run(main()) 