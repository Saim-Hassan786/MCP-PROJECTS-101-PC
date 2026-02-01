import asyncio
from typing import Optional, Any
from mcp import ClientSession , types
from mcp.client.streamable_http import streamablehttp_client
from contextlib import AsyncExitStack

class MCPClient:
    def __init__(self,server_url:str):
        self._server_url = server_url
        self._session : Optional[ClientSession] = None
        self._exit_session : AsyncExitStack = AsyncExitStack()

    async def connect(self):
        streaming_transport = await self._exit_session.enter_async_context(
            streamablehttp_client(self._server_url)
        )
        _read,_write,_session_id = streaming_transport
        self._session = await self._exit_session.enter_async_context(
            ClientSession(
                _read,
                _write
            )
        )
        await self._session.initialize()

    async def session(self) -> ClientSession:
        if self._session is None:
            raise ConnectionError("Connection Error")
        return self._session
    
    async def list_tools(self) -> types.ListToolsResult | list[None]:
        tools =  (await self._session.list_tools())
        return (tools.tools)
    
    async def call_tools(self,tool_name:str,tool_input:dict) -> types.CallToolRequest :
        return (await self._session.call_tool(tool_name,tool_input))
    
    async def cleanup(self):
        await self._exit_session.aclose()
        self._session = None
    
    async def __aenter__(self):
        await self.connect()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.cleanup()
    
async def main():
    async with MCPClient("http://127.0.0.1:8000/mcp") as client:
        tools = await client.list_tools()
        print(tools)

async def main_2():
    async with MCPClient("http://127.0.0.1:8000/mcp") as client2:
        tool_call = await client2.call_tools("Read Docs",tool_input = {"doc_id":"plan.md"})
        print(tool_call)

async def main_3():
    async with MCPClient("http://127.0.0.1:8000/mcp") as client3:
        tool_call = await client3.call_tools("Edit Docs",tool_input={"doc_id":"outlook.pdf","old_doc":"This document presents the projected future performance of the system.","new_doc":"My Plan Is to Become A Certified Agentic AI Engineer One Day"})
        print(tool_call)

asyncio.run(main())
asyncio.run(main_2())
asyncio.run(main_3())



