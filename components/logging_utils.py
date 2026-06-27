import aiofiles
import json
import os
import asyncio
from datetime import datetime

LOGS_DIR = os.environ.get("LOGS_DIR", "logs")

async def log_to_file(filename, content=None):
    if content is not None:
        if isinstance(content, dict) and "endpoint" in content:
            content["timestamp"] = datetime.now().isoformat()
            async with aiofiles.open(os.path.join(LOGS_DIR, filename), mode="a") as f:
                await f.write(json.dumps(content) + "\n")
        else:
            async with aiofiles.open(os.path.join(LOGS_DIR, filename), mode="a") as f:
                await f.write(str(content) + "\n")
    else:
        # Add trailing newline
        async with aiofiles.open(os.path.join(LOGS_DIR, filename), mode="a") as f:
            await f.write("\n")

async def log_inbound_chunk(filename, chunk, endpoint):
    await log_to_file(filename, {"endpoint": endpoint, "data": chunk})

async def log_outbound_chunk(filename, chunk, endpoint):
    await log_to_file(filename, {"endpoint": endpoint, "data": chunk})
