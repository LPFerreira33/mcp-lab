import os
import re
import asyncio
import json
from contextlib import AsyncExitStack
from typing import Any, Dict, List

import ollama
from dotenv import load_dotenv
from mcp import ClientSession
from mcp.client.sse import sse_client


# Load environment variables
load_dotenv()


SERVER_IP = os.getenv("SERVER_IP", "localhost") # Default to localhost if not set
SERVER_PORT = os.getenv("SERVER_PORT", "3312")

MODEL = os.getenv("MODEL", "hf.co/unsloth/Qwen3-30B-A3B-GGUF:Q4_K_M")  # Default model if not set

# Global variables to store session state
session = None
exit_stack = AsyncExitStack()



async def connect_to_server():
    """Connect to an MCP server.

    Args:
        server_script_path: Path to the server script.
    """
    global session, stdio, write, exit_stack

    
     # Connect to the server using SSE
    sse_url = f"http://{SERVER_IP}:{SERVER_PORT}/sse"

    # Connect to the server
    read_stream, write_stream = await exit_stack.enter_async_context(sse_client(sse_url))
    session = await exit_stack.enter_async_context(ClientSession(read_stream, write_stream))

    # Initialize the connection
    await session.initialize()

    # List available tools
    tools_result = await session.list_tools()
    print("\nConnected to server with tools:")
    for tool in tools_result.tools:
        print(f"  - {tool.name}: {tool.description}")


async def get_mcp_tools() -> List[Dict[str, Any]]:
    """Get available tools from the MCP server in OpenAI format.

    Returns:
        A list of tools in OpenAI format.
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


async def process_query(query: str) -> str:
    """Process a query using OpenAI and available MCP tools.

    Args:
        query: The user query.

    Returns:
        The response from OpenAI.
    """
    global session, openai_client, model

    # Get available tools
    tools = await get_mcp_tools()

    # import pprint
    # pp = pprint.PrettyPrinter()
    # pp.pprint(tools)
    
    system_prompt = (
        "You are a helpful assistant. "
        "If you need to use a tool, reply ONLY with a JSON object like "
        '{"<tool_name1>": "arguments": {...}, "<tool_name2>": "arguments": {...}, ...}. '
        "Otherwise, answer normally."
        "\nAvailable tools:\n"
    )
    for tool in tools:
        system_prompt += f"- {tool['function']['name']}: {tool['function']['description']}\n"
    
    
    response = ollama.chat(
            model=MODEL,
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': query},
            ]
        )

    content_no_think = re.sub(r'<think>.*?</think>\s*', '', response['message']['content'], flags=re.DOTALL)
    print("\ncontent_no_think:", content_no_think)
    
    

    try:
        tools_json = json.loads(content_no_think)
        print("tools_json:", tools_json)
    except (json.JSONDecodeError, TypeError):
        return response['message']['content']

    tool_results = {}
    for tool_name, arguments in tools_json.items():
        response = await session.call_tool(tool_name, arguments=arguments)
        tool_results.update({tool_name: response.content[0].text})
        
    print("tool_results:", tool_results)

    system_prompt = (
        "You are a helpful assistant. "
        "Use only the previous calculated tools results to answer the questions. Don't make up any new information and don't mention the tools on your response:"
        f"{tool_results}"
    )
    response = ollama.chat(
            model=MODEL,
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': query},
                
            ]
        )
    
    final_response = re.sub(r'<think>.*?</think>\s*', '', response['message']['content'], flags=re.DOTALL)
    
    return final_response
    

    
async def cleanup():
    """Clean up resources."""
    global exit_stack
    await exit_stack.aclose()


async def main():
    """Main entry point for the client."""
    await connect_to_server()

    # Example: Ask about company vacation policy
    query = "A person born on 1998-04-27 with 1.85m, what would be his age and height in feet?"
    # query = "What is the name of the current pope?"
    print(f"\nQuery: {query}")

    response = await process_query(query)
    print(f"\nResponse: {response}")

    await cleanup()


if __name__ == "__main__":
    asyncio.run(main())
