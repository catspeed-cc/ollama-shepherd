import asyncio
import json
import os
from datetime import datetime

LOGS_DIR = os.environ.get("LOGS_DIR", "logs")
ROUTER_TIMEOUT = float(os.environ.get("ROUTER_TIMEOUT", 900.0))

async def log_to_file(filename, content=None):
    loop = asyncio.get_running_loop()
    await loop.run_in_executor(None, _log_to_file_sync, filename, content)

def _log_to_file_sync(filename, content):
    if content is not None:
        if isinstance(content, dict) and "endpoint" in content:
            content["timestamp"] = datetime.now().isoformat()
            with open(os.path.join(LOGS_DIR, filename), mode="a") as f:
                f.write(json.dumps(content) + "\n")
        else:
            with open(os.path.join(LOGS_DIR, filename), mode="a") as f:
                f.write(str(content) + "\n")
    else:
        # Add trailing newline
        with open(os.path.join(LOGS_DIR, filename), mode="a") as f:
            f.write("\n")

async def log_inbound_chunk(filename, chunk, endpoint):
    await log_to_file(filename, {"endpoint": endpoint, "data": chunk})

async def log_outbound_chunk(filename, chunk, endpoint):
    await log_to_file(filename, {"endpoint": endpoint, "data": chunk})
