import asyncio
import json
import os
from datetime import datetime
from fastapi import Request
from .misc import join_path

LOG_ENABLED = os.environ.get("LOG_ENABLED", "False").lower() == "true"

LOGS_DIR = os.environ.get("LOGS_DIR", "logs")
ROUTER_TIMEOUT = float(os.environ.get("ROUTER_TIMEOUT", 900.0))

def get_endpoint_path(request: Request) -> str:
    """Safely extracts the endpoint path from the request."""
    route = request.scope.get("route")
    if route is not None:
        return route.path
    else:
        return request.url.path if request.url.path else "unknown"

async def log_to_file(filename, content=None):
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, _log_to_file_sync, filename, content)

def _log_to_file_sync(filename, content):
    if LOG_ENABLED:
        if content is not None:
            if isinstance(content, dict) and "endpoint" in content:
                content["timestamp"] = datetime.now().isoformat()
                with open(join_path(LOGS_DIR, filename), mode="a") as f:
                    f.write(json.dumps(content) + "\n")
            else:
                with open(join_path(LOGS_DIR, filename), mode="a") as f:
                    f.write(str(content) + "\n")
        else:
            # Add trailing newline
            with open(join_path(LOGS_DIR, filename), mode="a") as f:
                f.write("\n")

async def log_inbound_chunk(filename, chunk, endpoint):
    if LOG_ENABLED:
        await log_to_file(filename, {"endpoint": endpoint, "data": chunk})

async def log_outbound_chunk(filename, chunk, endpoint):
    if LOG_ENABLED:
        await log_to_file(filename, {"endpoint": endpoint, "data": chunk})
