from fastapi import Request
from fastapi.responses import JSONResponse, StreamingResponse
import httpx
import re
from .logging_utils import log_inbound_chunk, log_outbound_chunk, log_to_file
from .model_selection import get_target_port

async def proxy_show(request: Request):
    if request.method == "POST":
        data = await request.json()
    else:
        data = {}
    stream = data.get("stream", False)  # Respect original stream flag
    await log_inbound_chunk("aider.in.last.log", data)

    model = data.get("model", "")
    clean = re.sub(r'^ollama_chat/', '', model).strip()
    target = get_target_port(model)

    if target:
        try:
            async with httpx.AsyncClient(timeout=600.0) as client:
                async with client.stream("POST", f"{target}/api/show", json={"model": clean}) as resp:
                    async def stream_generator():
                        try:
                            async for line in resp.aiter_lines():
                                if line.strip():
                                    await log_outbound_chunk("aider.out.last.log", line)
                                    yield line
                        finally:
                            # Add trailing newline to log file after stream completes
                            await log_to_file("aider.out.last.log", "/api/show")

                    return StreamingResponse(stream_generator(), media_type="application/x-ndjson")
        except Exception as e:
            error_response = {"error": str(e)}
            await log_outbound_chunk("aider.out.last.log", error_response)
            return JSONResponse(error_response, status_code=500)

    response_data = {
        "model": clean,
        "modified_at": "2024-01-01T00:00:00Z",
        "size": 1000000000,
        "digest": "fake-digest",
        "details": {
            "format": "gguf",
            "family": "llama",
            "parameter_size": "70B" if "70b" in clean else "27B" if "27b" in clean else "9B",
            "quantization_level": "Q4_K_M"
        }
    }
    await log_outbound_chunk("aider.out.last.log", response_data)
    return response_data
