import os
import asyncio
from mcp import ClientSession
from mcp.client.sse import sse_client
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

SERVER_IP = os.getenv("SERVER_IP", "localhost") # Default to localhost if not set
SERVER_PORT = os.getenv("SERVER_PORT", "8050")

async def main():
    # Connect to the server using SSE
    sse_url = f"http://{SERVER_IP}:{SERVER_PORT}/sse"
    async with sse_client(sse_url) as (read_stream, write_stream):
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize the connection
            await session.initialize()

            # List available tools
            tools_result = await session.list_tools()
            print("Available tools:")
            for tool in tools_result.tools:
                print(f"  - {tool.name}: {tool.description}")

            # Call our calculator tool
            arguments = {"value": 3, "from_unit": "meters", "to_unit": "feet"}
            result = await session.call_tool("convert_length", arguments=arguments)
            print(f"{arguments['value']} {arguments['from_unit']} = {result.content[0].text} {arguments['to_unit']}")

if __name__ == "__main__":
    asyncio.run(main())
