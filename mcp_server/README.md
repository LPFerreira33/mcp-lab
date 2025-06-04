# MCP Server

## Setting Up Your Development Environment

Begin by preparing your environment. The MCP Python SDK equips you with all the necessary tools to develop both servers and clients.

```bash
# Create and activate a virtual environment
python -m venv .venv
source ./.venv/bin/activate

# Using uv (recommended)
uv pip install -r requirements.txt

# Or using pip
pip install -r requirements.txt
```

The MCP CLI tools provide helpful utilities for development and testing:

```bash
# Test a server with the MCP Inspector
mcp dev server.py

# Run a server directly
# mcp run server.py?
uv run server.py
```