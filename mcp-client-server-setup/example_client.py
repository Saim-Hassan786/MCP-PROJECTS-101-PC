import requests 
url = "http://127.0.0.1:8000/mcp"

payload = {
    "jsonrpc":"2.0",
    "method" : "tools/list",
    "params" : {},
    "id" : 1
}

payload_2 = {
    "jsonrpc":"2.0",
    "method" : "tools/call",
    "params" : {
        "name" : "Reading Docs",
        "arguments" : {
            "doc_name" : "deposition.md"
        }
    }
}

headers = {
    "Content-Type" :"application/json",
    "Accept" : "application/json, text/event-stream",
}

response = requests.post(url=url,json=payload,headers=headers)
print(response.text)


