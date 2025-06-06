# MCP Lab

This repository contains a modular setup for experimenting with MCP in Python. It includes both a server and a client, as well as reusable tool modules.

---

## Project Structure

```
mcp/
├── mcp_server/      # MCP server implementation and tools
│   ├── server.py
│   ├── requirements.txt
│   ├── README.md
│   └── tools/
│       └── ...
├── mcp_client/      # MCP client implementation
│   ├── client.py
│   ├── client_llm.py
│   ├── requirements.txt
│   ├── README.md
│   └── .env
├── LICENSE
└── README.md        # (This file)
```

---

## Quick Start

### 1. Clone the repository

```sh
git clone https://github.com/LPFerreira33/mcp-lab.git
cd mcp-lab
```

### 2. Set up the server

```sh
cd mcp_server
python -m venv .venv
source .venv/bin/activate
uv pip install -r requirements.txt
uv run server.py
```

### 3. Set up the client

```sh
cd mcp_client
python -m venv .venv
.venv\Scripts\activate
uv pip install -r requirements.txt
# Edit .env to match your server's IP and port if needed
python client.py
```

---

## Tool Modules

Reusable tools are organized in `mcp_server/tools/` and are automatically registered by the server. You can add your own tools by creating new Python functions in these modules.

---

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
