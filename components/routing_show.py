import httpx
import re
from fastapi import Request
from fastapi.responses import JSONResponse, StreamingResponse
from .logging_utils import log_inbound_chunk, log_outbound_chunk, log_to_file, ROUTER_TIMEOUT, get_endpoint_path
from .model_selection import get_target_port

async def proxy_show(request: Request):
    endpoint_path = get_endpoint_path(request)
    if request.method == "POST":
        data = await request.json()
    else:
        data = {}
    stream = data.get("stream", False)  # Respect original stream flag
    try:
        await log_inbound_chunk("aider.in.last.log", data, endpoint_path)
    except Exception as e:
        print(f"Error logging inbound chunk: {e}")

    model = data.get("model", "")
    clean = re.sub(r'^ollama_chat/', '', model).strip()
    target = get_target_port(model)

    if target:
        try:
            async with httpx.AsyncClient(timeout=ROUTER_TIMEOUT) as client:
                async with client.stream("POST", f"{target}/api/show", json={"model": clean}) as resp:
                    async def stream_generator():
                        try:
                            async for line in resp.aiter_lines():
                                if line.strip():
                                    try:
                                        await log_outbound_chunk("aider.out.last.log", line, endpoint_path)
                                    except Exception as e:
                                        print(f"Error logging outbound chunk: {e}")
                                    yield line
                        finally:
                            # Add trailing newline to log file after stream completes
                            try:
                                await log_to_file("aider.out.last.log", {"endpoint": endpoint_path})
                            except Exception as e:
                                print(f"Error logging to file: {e}")

                    return StreamingResponse(stream_generator(), media_type="application/x-ndjson")
        except Exception as e:
            error_response = {"error": str(e)}
            try:
                await log_outbound_chunk("aider.out.last.log", error_response, endpoint_path)
            except Exception as e:
                print(f"Error logging outbound chunk: {e}")
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
    try:
        await log_outbound_chunk("aider.out.last.log", response_data, endpoint_path)
    except Exception as e:
        print(f"Error logging outbound chunk: {e}")
    return response_data
