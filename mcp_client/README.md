# MCP Client

This directory contains a sample MCP client for connecting to an MCP server.

---

## Setup

1. **Create and activate a virtual environment:**
    ```sh
    python -m venv .venv
    .venv\Scripts\activate
    # source ./.venv/bin/activate  # linux
    ```

2. **Install dependencies:**
    ```sh
    pip install -r requirements.txt
    ```

---

## Configuration

Create a `.env` file in this directory with the following content (replace with your actual server details):

```
SERVER_IP=your_server_ip_here
SERVER_PORT=3312
```

**Note:**  
Do not share your `.env` file or any sensitive information publicly.

---

## Running the Client

Start the client with:

```sh
python client.py
```


---

## Notes

- Ensure your MCP server is running and accessible at the specified IP and port.