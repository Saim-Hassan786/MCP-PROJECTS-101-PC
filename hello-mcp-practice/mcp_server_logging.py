import asyncio
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.server import Context
from mcp import types

mcp = FastMCP(name="Logging-MCP-Server", stateless_http=False)

@mcp.tool(name = "log_event", description = "Log an event with a message")
async def lop_processor(ctx: Context, item_id:int, should_fail:bool) -> list[types.TextContent]:
    await ctx.debug(f"Starting the logging process.{item_id}")
    await asyncio.sleep(0.5)
    await ctx.info(f"Logging item {item_id} with should_fail={should_fail}")
    await asyncio.sleep(0.5)
    if should_fail:
        await ctx.warning(f"Simulated failure for item {item_id}")
        await asyncio.sleep(0.5)
        await ctx.error(f"Error occurred while processing item {item_id}")
        return [types.TextContent(type="text", text=f"Failed to log item {item_id}")]


    await ctx.info(f"Successfully logged item {item_id}")
    return [types.TextContent(type="text", text=f"Successfully logged item {item_id}")]

mcp_app = mcp.streamable_http_app()