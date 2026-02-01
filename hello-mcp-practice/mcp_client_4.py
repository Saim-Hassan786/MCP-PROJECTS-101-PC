import asyncio
from typing import Any, Optional
from mcp.client.streamable_http import streamablehttp_client
from mcp import ClientSession, types
from contextlib import AsyncExitStack
from pydantic import AnyUrl

import json
from bs4 import BeautifulSoup


class MCPClient:
    def __init__(self, server_url : str):
        self.server_url = server_url
        self.sess : Optional[ClientSession] = None
        self.manage_session : AsyncExitStack = AsyncExitStack()

    async def connect(self):
        streaming_transport = await self.manage_session.enter_async_context(
            streamablehttp_client(self.server_url)
        )
        read,write,transport_id = streaming_transport
        self.sess = await self.manage_session.enter_async_context(
            ClientSession(read_stream=read,write_stream=write)
        ) 
        await self.sess.initialize()

    async def session(self) -> ClientSession:
        if self.sess is None:
            raise ConnectionError("Connection is Not Established")
        return self.sess
    
    async def list_tools(self) -> types.ListToolsResult | list[None]:
        assert self.sess , "Session Not Available"
        result = await self.sess.list_tools()
        return result.tools
    
    async def tool_call(self,tool_name:str,tool_input:dict[str,Any]) -> types.CallToolRequest:
        assert self.sess , "Session Not Available" 
        result = await self.sess.call_tool(tool_name,tool_input)
        return result
    
    async def list_resource(self):
        assert self.sess, "Session Not Available"
        result = await self.sess.list_resources()
        return result
    
    async def list_prompts(self):
        assert self.sess, "Session Not Available"
        result = await self.sess.list_prompts()
        return result.prompts
    
    async def get_prompts(self,name:str ,arguments : dict[str,Any]):
        assert self.sess, "Session Not Available"
        try:
            result = await self.sess.get_prompt(name=name, arguments=arguments)
            return result
        except Exception as e:
            return {"error": str(e)}
    

# =============================== SIMPLE ONES =======================================================
    # async def read_resource(self, uri):
    #     assert self.sess , "Session Not Available"
    #     result = await self.sess.read_resource(uri=uri)
    #     return result

    # async def read_resource(self, doc_id: Optional[str] = None):
    #     assert self.sess, "Session Not Available"
    #     uri = "docs://documents" if doc_id is None else f"docs://documents/{doc_id}"
    #     try:
    #         result = await self.sess.read_resource(uri=AnyUrl(uri))
    #         return result.contents[0]
    #     except Exception as e:
    #         print(f"Error reading resource for URI '{uri}': {e}")
    #         raise
# ===============================================================================================================

    async def read_resource(self, uri: str):
        assert self.sess, "Session Not Available"

        try:
            result = await self.sess.read_resource(uri=uri)

            if not getattr(result, "contents", []):
                return {"success": False, "error": "No content returned"}

            parsed_outputs = []

            for content in result.contents:
                text_data = getattr(content, "text", "") or ""

                if (content.mimeType and "json" in content.mimeType) or text_data.strip().startswith(("{", "[")):
                    try:
                        parsed_json = json.loads(text_data)
                        text_data = json.dumps(parsed_json, indent=2)
                    except json.JSONDecodeError:
                        pass

                elif "<html" in text_data.lower():
                    soup = BeautifulSoup(text_data, "html.parser")
                    text_data = soup.get_text(separator="\n", strip=True)

                parsed_outputs.append({
                    "mime_type": getattr(content, "mimeType", None),
                    "text": text_data
                })

            return {
                "success": True,
                "uri": uri,
                "contents": parsed_outputs
            }

        except Exception as e:
            return {
                "success": False,
                "uri": uri,
                "error": str(e)
            }

    async def list_template_resources(self):
        assert self.sess , "Session Not Available"
        result = await self.sess.list_resource_templates()
        return result
    
    async def cleanup(self):
        assert self.sess , "Session Not Available"
        await self.manage_session.aclose()
        self.sess = None

    async def __aenter__(self):
        await self.connect()
        return self
    
    async def __aexit__(self,exc_type,exc_val,exc_tb):
        await self.cleanup()

async def main():
    async with MCPClient("http://127.0.0.1:8000/mcp") as client:
        result = await client.list_tools()
        print (result)

async def main_2():
    async with MCPClient("http://127.0.0.1:8000/mcp") as client2:
        result = await client2.list_resource()
        print(result)

async def main_3():
    async with MCPClient("http://127.0.0.1:8000/mcp") as client3:
        result = await client3.read_resource(uri="docs://documents")
        print(result.contents[0].text)

async def main_4():
    async with MCPClient("http://127.0.0.1:8000/mcp") as client4:
        result = await client4.list_template_resources()
        print(result)

async def main_5():
    async with MCPClient("http://127.0.0.1:8000/mcp") as client:
        print(await client.read_resource(uri="http://fetch/example/docs")) 

async def main_6():
    async with MCPClient("http://127.0.0.1:8000/mcp") as client:
        result = await client.list_prompts()
        print(result)

async def main_7():
    async with MCPClient("http://127.0.0.1:8000/mcp") as client:
        result = await client.get_prompts(name="Format Docs",arguments={"doc_id":"plan.md"})
        print(result)

asyncio.run(main_7())


        