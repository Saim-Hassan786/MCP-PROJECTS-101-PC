import platform
from urllib.parse import unquote
from pathlib import Path
from urllib.parse import urlparse

from mcp.server.fastmcp import FastMCP, Context
from mcp.types import TextContent

mcp = FastMCP(
    name="mcp-roots-server",
    stateless_http=False
)


@mcp.tool()
async def analyze_project(ctx: Context) -> TextContent:
    print("-> Server: Requesting project roots from client...")
    roots = await ctx.session.list_roots()

    if not roots or not roots.roots:
        return TextContent(text="No project roots found", type="text")

    root = roots.roots[0] 
    print(f"<- Server: Received root: {root.uri}")
    
    uri_str = str(root.uri)
    if platform.system() == "Windows" and uri_str.startswith("file://"):
        if uri_str.startswith("file:///"):
            path_str = unquote(uri_str[8:])  
        else:
            path_str = unquote(uri_str[7:]) 
            if path_str.startswith('/') or path_str.startswith('\\'):
                path_str = path_str[1:]  
        path = Path(path_str)
    else:
        path = Path(urlparse(str(root.uri)).path)

    py_files = list(path.glob("*.py"))

    analysis = f"Found {len(py_files)} Python files in project at {path}"
    print(f"-> Server: Analysis complete: {analysis}")

    return TextContent(text=analysis, type="text")

mcp_app = mcp.streamable_http_app()


