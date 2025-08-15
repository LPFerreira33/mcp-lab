import logging
import inspect

from mcp.server.fastmcp import FastMCP

import tools.itemtracker_tools as itemtracker_tools

# Simple logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create MCP server
mcp = FastMCP(
    name="Utility Toolkit",
    description="Collection of useful tools",
    host="localhost",
    port=3312,
)

# Register all functions from itemtracker_tools
for name, func in inspect.getmembers(itemtracker_tools, inspect.isfunction):
    mcp.tool()(func)
    logger.info(f"Registered tool: {name}")

def main():
    """Run the MCP server."""
    try:
        logger.info("Starting Utility Toolkit MCP server on port 3312")
        mcp.run(transport="sse")
    except KeyboardInterrupt:
        logger.info("Server stopped (KeyboardInterrupt)")
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise

if __name__ == "__main__":
    main()