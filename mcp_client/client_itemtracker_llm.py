import os
import re
import json
import time
from contextlib import AsyncExitStack
from typing import Any, Dict, List

import ollama
from dotenv import load_dotenv
from mcp import ClientSession
from mcp.client.sse import sse_client

import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# --- Configuration and Globals ---

def load_config():
    load_dotenv()
    return {
        "SERVER_IP": os.getenv("SERVER_IP", "localhost"),
        "SERVER_PORT": os.getenv("SERVER_PORT", "3312"),
        "MODEL": os.getenv("MODEL", "hf.co/unsloth/Phi-4-mini-instruct-GGUF:Q4_K_M"),
    }

config = load_config()
exit_stack = AsyncExitStack()
session: ClientSession | None = None

# --- MCP Server Connection ---

async def connect_to_server():
    """
    Connect to the MCP server and initialize the session.
    """
    global session, exit_stack
    
    sse_url = f"http://{config['SERVER_IP']}:{config['SERVER_PORT']}/sse"
    read_stream, write_stream = await exit_stack.enter_async_context(sse_client(sse_url))
    session = await exit_stack.enter_async_context(ClientSession(read_stream, write_stream))
    await session.initialize()
    tools_result = await session.list_tools()
    
    print("\nConnected to server with tools:")
    for tool in tools_result.tools:
        print(f"  - {tool.name}: {tool.description}")

async def cleanup():
    """
    Clean up resources by closing the async exit stack.
    """
    global exit_stack
    await exit_stack.aclose()

# --- Tool Utilities ---

async def get_mcp_tools() -> List[Dict[str, Any]]:
    """
    Retrieve the available tools from the MCP server and format them in OpenAI-compatible format.

    Returns:
        List[Dict[str, Any]]: A list of tools, each represented as a dictionary with type, function name, description, and parameters.
    """
    global session

    tools_result = await session.list_tools()
    return [
        {
            "type": "function",
            "function": {
                "name": tool.name,
                "description": tool.description,
                "parameters": tool.inputSchema,
            },
        }
        for tool in tools_result.tools
    ]

async def get_llm_tool_json(query: str, try_extract_json: bool = False) -> dict | str:
    """
    Query the LLM with the user query and available tools, and extract the tool call JSON from the LLM's response.

    Args:
        query (str): The user's query.
        try_extract_json (bool): If True, try to extract a JSON/dict from the response even if not valid JSON.

    Returns:
        dict | str: The extracted JSON object if valid, otherwise the raw response string.
    """
    tools = await get_mcp_tools()
    system_prompt = (
        "You are a helpful assistant that helps track items taking into account the user ask. "
        "You need to use a tool. Don't use any formating. Reply ONLY with a JSON object like "
        '{"<tool_name>": {"<argument0>": "<value0>",...} '
        "\nAvailable tools:\n"
    )
    for tool in tools:
        system_prompt += f"- {tool['function']['name']}: {tool['function']['description']}\n"

    response = ollama.chat(
        model=config["MODEL"],
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': query},
        ]
    )
    print("Response from model:", response['message']['content'])

    try:
        tools_json = json.loads(response['message']['content'])
        print("tools_json:", tools_json)
        return tools_json
    except (json.JSONDecodeError, TypeError):
        if try_extract_json:
            # If JSON extraction is requested and the response is not valid JSON,
            # try to extract a JSON-like string from the response
            # match from the first "{" to the last "}"
            match = re.search(r'(\{.*\})', response['message']['content'], re.DOTALL)
            if match:
                json_str = match.group(1)
                try:
                    tools_json = json.loads(json_str)
                    print("tools_json (extracted):", tools_json)
                    return tools_json
                except Exception:
                    return response['message']['content']
        return response['message']['content']


async def call_tools_with_json(tools_json: dict) -> dict:
    """
    Call the MCP tools specified in the JSON and return their results.

    Args:
        tools_json (dict): A dictionary mapping tool names to their arguments.

    Returns:
        dict: A dictionary mapping tool names to their call results.
    """
    tool_results = {}
    for tool_name, arguments in tools_json.items():
        response = await session.call_tool(tool_name, arguments=arguments)
        tool_results[tool_name] = response.content[0].text
    print("tool_results:", tool_results)
    return tool_results

# --- FastAPI App ---

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your domains
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PromptRequest(BaseModel):
    prompt: str

class ToolCallRequest(BaseModel):
    tool_call: dict

@app.on_event("startup")
async def startup_event():
    await connect_to_server()

@app.on_event("shutdown")
async def shutdown_event():
    await cleanup()

@app.post("/get_toolcall")
async def get_toolcall(request: PromptRequest):
    start_time = time.time()
    print(f"MODEL being used: {config['MODEL']}")
    try:
        result = await get_llm_tool_json(query=request.prompt, try_extract_json=True)
        elapsed = time.time() - start_time
        print(f"Elapsed time for get_toolcall: {elapsed:.2f} seconds")
        return {"tool_call": result}
    except Exception:
        elapsed = time.time() - start_time
        print(f"Elapsed time for get_toolcall (error): {elapsed:.2f} seconds")
        raise HTTPException(status_code=400, detail="Prompt could not be understood as a tool call.")

@app.post("/execute_toolcall")
async def execute_toolcall(request: ToolCallRequest):
    try:
        tools_result = await call_tools_with_json(tools_json=request.tool_call)
        return {"tools_result": tools_result}
    except Exception:
        raise HTTPException(status_code=500, detail="Internal Server error")

# --- Main Entrypoint for Standalone Usage ---

async def main():
    """
    Main entry point for the client. Connects to the server, processes a sample query, and cleans up resources.
    """
    await connect_to_server()

    # query = "Add Canned Tuna with replacement date in 25th June 2025 and expiration date in 25th June 2025 into storage named Bunker 101"
    query = "Adiciona Pao com data de substituição a 25 de Junho de 2025 e data de validade a 26 de Junho de 2025 no armazemento: mochila do Joao"
    # query = "Edita item com id 21 para data de validade a 26 de Junho de 2025"
    # query = "Remove item com id 21"
    print(f"\nQuery: {query}")
    
    tools_json = await get_llm_tool_json(query)
    
    if not isinstance(tools_json, dict):
        return tools_json  # Return raw response if not valid JSON
    
    response = await call_tools_with_json(tools_json)
    
    print(f"\nResponse: {response}")

    await cleanup()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3313)
