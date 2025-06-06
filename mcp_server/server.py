import logging
import inspect
import importlib
import pkgutil

from mcp.server.fastmcp import FastMCP

import tools


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

# Dynamically import all modules in the 'tools' package
tool_modules = []
for _, module_name, is_pkg in pkgutil.iter_modules(tools.__path__):
    if not is_pkg:
        module = importlib.import_module(f"tools.{module_name}")
        tool_modules.append(module)
        logger.info(f"Imported tool module: {module_name}")

# Dynamically register all functions from the tool modules
for module in tool_modules:
    for name, func in inspect.getmembers(module, inspect.isfunction):
        mcp.tool()(func)
        logger.info(f"Registered tool: {name}")

def main():
    """Run the MCP server."""
    try:
        logger.info("Starting Utility Toolkit MCP server on port 8050")
        mcp.run(transport="sse")
    except KeyboardInterrupt:
        logger.info("Server stopped (KeyboardInterrupt)")
    except Exception as e:
        logger.error(f"Server error: {e}")
        raise

if __name__ == "__main__":
    main()