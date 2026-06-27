from fastapi import Request
from fastapi.responses import StreamingResponse, JSONResponse
import httpx
import json
from .logging_utils import log_inbound_chunk, log_outbound_chunk, log_to_file
from .model_selection import get_target_port

async def proxy_chat(request: Request):
    endpoint_path = request.scope.route.path
    data = await request.json()
    await log_inbound_chunk("aider.in.last.log", data, endpoint_path)

    model = data.get("model", "")
    stream = data.get("stream", False)  # Respect original stream flag

    target = get_target_port(model)
    if not target:
        error_response = {"error": f"Unknown model: {model}"}
        await log_outbound_chunk("aider.out.last.log", error_response, endpoint_path)
        return JSONResponse(error_response, status_code=400)

    print(f"DEBUG: Routing '{model}' to {target} (stream={stream})")

    # NON-STREAMING: Wait for full response, return single JSON
    if not stream:
        try:
            async with httpx.AsyncClient(timeout=600.0) as client:
                resp = await client.post(f"{target}/api/chat", json=data)
                resp.raise_for_status()
                response_data = resp.json()
                await log_outbound_chunk("aider.out.last.log", response_data, endpoint_path)
                return JSONResponse(content=response_data)
        except Exception as e:
            error_response = {"error": str(e)}
            await log_outbound_chunk("aider.out.last.log", error_response, endpoint_path)
            return JSONResponse(error_response, status_code=500)

    # STREAMING: Forward NDJSON chunks immediately
    async def stream_generator():
        try:
            async with httpx.AsyncClient(timeout=600.0) as client:
                async with client.stream("POST", f"{target}/api/chat", json=data) as resp:
                    async for line in resp.aiter_lines():
                        if line.strip():
                            await log_outbound_chunk("aider.out.last.log", line, endpoint_path)
                            yield line
        finally:
            # Add trailing newline to log file after stream completes
            await log_to_file("aider.out.last.log", {"endpoint": endpoint_path})

    return StreamingResponse(stream_generator(), media_type="application/x-ndjson")
