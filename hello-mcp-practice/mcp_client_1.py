import httpx
import json
import asyncio
from typing import Any

async def mcp_request(method:str , params:dict[str,Any] | None = None):
    payload = {
        "jsonrpc" : "2.0",
        "method" : method,
        "params" : params or {},
        "id" : 1
    }
    headers = {
        "Content-Type" : "application/json",
        "Accept" : "application/json, text/event-stream"
    }

    try:
        async with httpx.AsyncClient() as client:
            async with client.stream(
                "POST",
                "http://localhost:8000/mcp",
                json = payload,
                headers = headers,
                timeout = 10
            ) as response:
                print(f"   -> Sending {method} request...")
                response.raise_for_status()

                async for line in response.aiter_lines():
                    print(f"   <- Received raw data: {line}")
                    if line.startswith("data: "):
                        line = line[6:]
                        print(f"   <- Received data: {line}")
                        return json.loads(line)
        return {"error" : "No Data Received For The Request"}
    except Exception as e:
        print(f"   -> An error occurred: {e}")
        return {"error": str(e)}
    
async def main():
    print("We send a 'tools/list' request to discover available tools.")
    mcp_server_response = await mcp_request("tools/list")
    print(f"MCP-Server-Response : {mcp_server_response}")

if __name__ == "__main__":
    asyncio.run(main())