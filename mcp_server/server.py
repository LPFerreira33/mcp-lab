import logging
from mcp.server.fastmcp import FastMCP

# Import tools from separate modules
import inspect
import tools.conversion_tools as conversion_tools
import tools.text_tools as text_tools
import tools.utility_tools as utility_tools


# Simple logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create MCP server
mcp = FastMCP(
    name="Utility Toolkit",
    description="Collection of useful conversion, text, and utility tools",
    host="0.0.0.0",
    port=8050,
)


# List of modules to scan for tool functions
tool_modules = [conversion_tools, text_tools, utility_tools]

# Dynamically register all functions from the tool modules
for module in tool_modules:
    for name, func in inspect.getmembers(module, inspect.isfunction):
        mcp.tool()(func)
        logger.info(f"Registered tool: {name}")

def main():
    """Run the MCP server."""
    try:
        logger.info("Starting Utility Toolkit MCP server on port 8050")
        logger.info("Available tools: length converter, temperature converter, currency converter, word counter, password generator, age calculator, timezone info")
        mcp.run(transport="sse")
    except KeyboardInterrupt:
        logger.info("Server stopped (KeyboardInterrupt)")
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise

if __name__ == "__main__":
    main()