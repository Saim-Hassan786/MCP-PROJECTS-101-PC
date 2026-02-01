import asyncio
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.server import Context

mcp = FastMCP(name="Progress-MCP-Server", stateless_http=False)

@mcp.tool(name = "long_task", description = "A long-running task that reports progress")
async def long_task_processor(ctx: Context,file_name:str,mb_size:int) -> str:
    await ctx.debug(f"Starting long task for file: {file_name} of size {mb_size}MB")
    await asyncio.sleep(0.5)
    await ctx.info(f"Preparing to process file: {file_name}")
    await asyncio.sleep(0.5)

    total_steps = mb_size * 10
    for step in range(total_steps + 1):
        progress = step
        percentage = (step / total_steps) * 100

        await ctx.report_progress(
            progress=progress,
            total=total_steps,
            message=f"Processing {file_name}: {percentage:.2f}% complete"
        )
        await asyncio.sleep(0.1)
    
    await ctx.info(f"Completed processing file: {file_name}")
    return f"File {file_name} of size {mb_size}MB processed successfully."

@mcp.tool(name = "process_data", description = "A data showing progress function")
async def process_data(ctx: Context, data:int) -> str:
    await ctx.info(f"Starting Processing data: {data}")
    await asyncio.sleep(0.5)
    for i in range(data+1):
        if i == 0:
            message = "Starting data processing"
        elif i < data // 4:
            message = "Loading and validating records..."
        elif i < data // 2:
            message = "Applying transformations..."
        elif i < data * 3 // 4:
            message = "Running calculations..."
        else:
            message = "Finalizing results..."

        await ctx.report_progress(
            progress=i,
            total=data,
            message=message
        )
        await asyncio.sleep(0.1)

    await ctx.info(f"Completed processing data: {data}")
    return f"Data {data} processed successfully."

mcp_app = mcp.streamable_http_app()


