import asyncio
from pathlib import Path
from pydantic import FileUrl

from mcp.shared.context import RequestContext
from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client
from mcp.types import Root, ListRootsResult, ErrorData

def _create_roots(root_paths: list[str]) -> list[Root]:
    roots = []
    for path in root_paths:
        p = Path(path).resolve()
        # Fix for Windows: use file:/// and forward slashes
        path_str = str(p).replace('\\', '/')
        file_url = FileUrl(f"file:///{path_str}")
        roots.append(Root(uri=file_url, name=p.name or "Root"))
    return roots

async def _handle_list_roots(
    context: RequestContext["ClientSession", None]
) -> ListRootsResult | ErrorData:
    root_paths = [str(Path.cwd().absolute())]
    return ListRootsResult(roots=_create_roots(root_paths))


async def main():
    server_url = "http://localhost:8000/mcp/"
    print(f"🚀 Connecting to MCP server at {server_url}")

    try:
        async with streamablehttp_client(server_url) as (read_stream, write_stream, get_session_id):

            async with ClientSession(read_stream, write_stream, list_roots_callback=_handle_list_roots) as session:
                print("✅ Connected. Initializing session...")
                await session.initialize()
                print("🛠️ Session initialized with roots capability.")

                print("\n-> Client: Calling analyze_project tool...")
                result = await session.call_tool("analyze_project")

                print("\n🔍 Project Analysis Results:", result)

    except Exception as e:
        print(f"\n❌ An error occurred: {e}")

    print("\n✅ Demo complete!")

if __name__ == "__main__":
    asyncio.run(main())