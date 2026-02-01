import requests

url = "http://localhost:8000/mcp/"

payload = {
    "jsonrpc": "2.0",
    "id": "1",
    "method": "initialize",
    "params": {
        "protocolVersion": "2025-06-18",
        "capabilities": {
            "roots": {},
            "sampling": {},
            "elicitation": {},
            },
        "clientInfo": {
            "name": "MCP Client",
            "version": "1.0.0",
            "title": "MCP Client Example"
            }
        }
}


headers = {
    "Content-Type" :"application/json",
    "Accept" : "application/json, text/event-stream",
    "MCP-Protocol-Version": "2025-06-18",
}

response = requests.post(url, json=payload, headers=headers)
print(response.headers)
print(response.text)
session_id = response.headers.get("mcp-session-id")
print("Session ID:", session_id)


next_headers = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",
    "MCP-Protocol-Version": "2025-06-18",
    "mcp-session-id": session_id,  
}

payload = {
    "jsonrpc": "2.0",
    "method": "notifications/initialized"
}

response = requests.post(url, json=payload, headers=next_headers)
print(response)

headers_tool_list = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",
    "MCP-Protocol-Version": "2025-06-18",
    "mcp-session-id": session_id,
}

payload_tool_list = {
    "jsonrpc": "2.0",
    "method": "tools/list",
    "params": {},
    "id": "1"
}

response = requests.post(url, json=payload_tool_list, headers=headers_tool_list)
print(response.text)

headers_tool_run = {
    "Content-Type": "application/json",
    "Accept": "application/json, text/event-stream",
    "MCP-Protocol-Version": "2025-06-18",
    "mcp-session-id": session_id,
}

payload_tool_run = {
    "jsonrpc": "2.0",
    "method": "tools/call",
    "params": {
        "name": "weather_tool",
        "arguments": {
            "city": "Lahore",
        }
    },
    "id": "2"
}

response = requests.post(url, json=payload_tool_run, headers=headers_tool_run)
print(response.text)