import requests
from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.prompts import base
from mcp.types import PromptMessage, TextContent

mcp = FastMCP(
    name = "MCP_Server_2",
    stateless_http = True
)

docs = {
    "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
    "report.pdf": "The report details the state of a 20m condenser tower.",
    "financials.docx": "These financials outline the project's budget and expenditures.",
    "outlook.pdf": "This document presents the projected future performance of the system.",
    "plan.md": "The plan outlines the steps for the project's implementation.",
    "spec.txt": "These specifications define the technical requirements for the equipment.",
}


# TOOLS
@mcp.tool(name="Read Docs",description="A Reading Tool to read the doc")
async def read_doc(doc_id:str):
    if doc_id not in docs:
        raise ValueError(f"{doc_id} Not Found")
    doc = docs[doc_id]
    return doc

@mcp.tool(name="Edit Docs",description="An Editing Tool to edit the doc")
async def edit_doc(doc_id:str,old_doc:str,new_doc:str):
    global docs
    if doc_id not in docs:
        raise ValueError(f"{doc_id} Not Found")
    docs[doc_id] = docs[doc_id].replace(old_doc,new_doc)
    return docs[doc_id]
    # return f"Successfully Updated Docs {doc_id}"

# Resources
@mcp.resource(uri="docs://documents",name="Docs Data",description="Documents Data",mime_type="application/json")
async def read_docs():
    doc = list(docs.keys())
    return doc


@mcp.resource(uri="docs://documents/{doc_id}", name="Docs Id Data", description="Docs Id Data", mime_type="application/json")
async def read_docs_with_id(doc_id: str):
    if doc_id in docs:
        return {"name": doc_id, "content": docs[doc_id]}
    else:
        raise ValueError(f"Document '{doc_id}' not found.")
    
    
@mcp.resource(uri="http://fetch/example/docs", name="Webpage Data", description="Fetches content from a webpage at a given URL", mime_type="text/plain")
async def read_webpage():
    try:
        response = requests.get(url="http://example.com", timeout=5)
        response.raise_for_status()  # Raises an error for bad HTTP status codes
        return response.text
    except Exception as e:
        raise ValueError(f"Could not fetch webpage : {str(e)}")


# Prompts  
@mcp.prompt(name="Format Docs",description="A Prompt to get the docs",title="MCP Format Prompt")
async def format_docs(doc_id: str):
    prompt = f"""
You are a helpful assistant.Your job is to format the document {doc_id} in a markdown format.
Use the following format:
# Document: {doc_id}
Always include Bold headings for each section and use bullet points for lists.
The markdown should be well structured and easy to read.
"""
    return [base.UserMessage(prompt)]

@mcp.prompt(name="Summarize Docs",description="A Prompt to summarize the docs",title="MCP Summarize Docs Prompt")
async def summarize_docs(doc_id: str):
    prompt = f"""
You are a helpful assistant. Your job is to summarize the document {doc_id} in a concise manner.
Use the following format:
# Summary of {doc_id}
Always include the main points and key information.
The summary should be clear and to the point.
"""
    return PromptMessage(
        role="user",
        content=TextContent(
            type="text",
            text=prompt          
        )
    )

mcp_app = mcp.streamable_http_app()



# =========================================================================================================
# Run the Code Below After Uncommenting To See The Edited Version Of the Docs in the File Save As Session's Restart Each Time Result in the Loss Od In Memory Edits

# import json
# import os
# if not os.path.exists('docs.json'):
#     docs = {
#         "deposition.md": "This deposition covers the testimony of Angela Smith, P.E.",
#         "report.pdf": "The report details the state of a 20m condenser tower.",
#         "financials.docx": "These financials outline the project's budget and expenditures.",
#         "outlook.pdf": "This document presents the projected future performance of the system.",
#         "plan.md": "The plan outlines the steps for the project's implementation.",
#         "spec.txt": "These specifications define the technical requirements for the equipment.",
#     }
#     with open('docs.json', 'w') as f:
#         json.dump(docs, f)

# @mcp.tool(name="Edit Docs",description="An Editing Tool to edit the doc")
# async def edit_doc(doc_id:str,old_doc:str,new_doc:str):
#     with open('docs.json', 'r') as f:
#         docs = json.load(f)
#     if doc_id not in docs:
#         raise ValueError(f"{doc_id} Not Found")
#     docs[doc_id] = docs[doc_id].replace(old_doc,new_doc)
#     with open('docs.json', 'w') as f:
#         json.dump(docs, f)
#     return docs[doc_id]
# =========================================================================================================