import httpx
import json
import asyncio
from typing import Any

async def client_request(method:str, params:dict[str,Any]|None = None):
    payload = {
        "jsonrpc" : "2.0",
        "method" : method,
        "params" : params,
        "id" : 1
    }
    headers = {
        "Content-Type" : "application/json",
        "Accept" : "application/json, text/event-stream"
    }
    async with httpx.AsyncClient() as client:
        async with client.stream(
            "POST",
            "http://localhost:8000/mcp",
            json=payload,
            headers=headers,
            timeout=10
        ) as response:
            print(f"Sending {method} To Server")
            response.raise_for_status()

            async for line in response.aiter_lines():
                if line:  # Skip empty lines
                    print(f"   <- Received raw data: {line}")
                    if line.startswith("data: "):
                        line = line[6:]
                        print(f"   <- Received data: {line}")
                        return json.loads(line)



async def main():
    print("Calling the Server With Client")
    server_response = await client_request(
        method="tools/list",
        params={}
    )
    print("Final Result ", server_response)



# For Tool Calls
async def main_1():
    print("Calling the Server With Client")
    server_response_1 = await client_request(
        method="tools/call",
        params={
            "name" : "greeting_tool",
            "arguments" : {
                "name" : "Saim Hassan"
            }
        }
    )
    print("Final Result ", server_response_1)

async def main_2():
    print("Calling the Server With Client")
    server_response_2 = await client_request(
        method="tools/call",
        params={
            "name": "addition_tool",
            "arguments" : {
                "a" : 25,
                "b" : 25
            }
        }
    )
    print("Final Result ", server_response_2)


async def main_3():
    print("Calling the Server With Client")
    server_response_3 = await client_request(
        method="tools/call",
        params={
            "name" : "user_info_tool",
            "arguments" : {
                "name" : "Saim Hassan",
                "age" : 25
            }
        }
    )
    print("Final Result ", server_response_3)



asyncio.run(main())
asyncio.run(main_1())
asyncio.run(main_2())
asyncio.run(main_3())