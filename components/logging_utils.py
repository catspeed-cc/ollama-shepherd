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
    if content is None:
        await loop.run_in_executor(None, _log_to_file_sync, filename, None, True)
    else:
        await loop.run_in_executor(None, _log_to_file_sync, filename, content)

def _log_to_file_sync(filename, content, end_of_stream=False):
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

        if end_of_stream:
            # Rotate log file
            log_dir = os.path.dirname(join_path(LOGS_DIR, filename))
            base_filename = os.path.basename(filename)
            files = [f for f in os.listdir(log_dir) if f.startswith(base_filename + '.')]

            # Sort files by number (if any)
            numbered_files = []
            for f in files:
                parts = f.split('.')
                if len(parts) > 1 and parts[1].isdigit():
                    numbered_files.append((int(parts[1]), f))
            numbered_files.sort(key=lambda x: x[0])

            # Determine next number
            next_number = 1
            if numbered_files:
                next_number = numbered_files[-1][0] + 1

            # Move log file to new location
            new_filename = f"{base_filename}.{next_number}"
            os.rename(join_path(LOGS_DIR, filename), join_path(LOGS_DIR, new_filename))

async def log_inbound_chunk(filename, chunk, endpoint):
    if LOG_ENABLED:
        await log_to_file(filename, {"endpoint": endpoint, "data": chunk})

async def log_outbound_chunk(filename, chunk, endpoint):
    if LOG_ENABLED:
        await log_to_file(filename, {"endpoint": endpoint, "data": chunk})
