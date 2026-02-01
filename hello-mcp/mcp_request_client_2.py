import requests

url = "http://127.0.0.1:8000/mcp/"

headers = {
     "Accept" : "application/json,text/event-stream"
}

body = {
    "jsonrpc" : "2.0",
    "id"  : 1,
    "method" : "tools/call",
    "params" : {
        "name" : "Info Tool",
        "arguments" : {
            "name" : "Saim Hassan",
            "age"  : 25
        }
    } 
}

response = requests.post(url=url,headers=headers,json=body)

print(response.text)
for lines in response.iter_lines():
     if lines:
          print(lines)