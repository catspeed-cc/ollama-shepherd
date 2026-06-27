import aiofiles
import json
import os
import asyncio

LOGS_DIR = os.environ.get("LOGS_DIR", "logs")

async def log_to_file(filename, content=None):
    async with aiofiles.open(os.path.join(LOGS_DIR, filename), mode="a") as f:
        if content is not None:
            await f.write(json.dumps(content) + "\n")
        else:
            # Add trailing newline
            await f.write("\n")

async def log_inbound_chunk(filename, chunk, endpoint):
    await log_to_file(filename, chunk)

async def log_outbound_chunk(filename, chunk, endpoint):
    await log_to_file(filename, chunk)
