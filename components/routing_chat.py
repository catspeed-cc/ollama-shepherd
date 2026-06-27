from fastapi import Request
from fastapi.responses import StreamingResponse, JSONResponse
import httpx
import json
from .logging_utils import log_to_file
from .model_selection import get_target_port

async def proxy_chat(request: Request):
    data = await request.json()
    log_to_file("aider.in.last.log", "/api/chat", data, stream=False)

    model = data.get("model", "")
    stream = data.get("stream", False)  # Respect original stream flag

    target = get_target_port(model)
    if not target:
        error_response = {"error": f"Unknown model: {model}"}
        log_to_file("aider.out.last.log", "/api/chat", error_response, stream=False)
        return JSONResponse(error_response, status_code=400)

    print(f"DEBUG: Routing '{model}' to {target} (stream={stream})")

    # NON-STREAMING: Wait for full response, return single JSON
    if not stream:
        try:
            async with httpx.AsyncClient(timeout=600.0) as client:
                resp = await client.post(f"{target}/api/chat", json=data)
                resp.raise_for_status()
                response_data = resp.json()
                log_to_file("aider.out.last.log", "/api/chat", response_data, stream=False)
                return JSONResponse(content=response_data)
        except Exception as e:
            error_response = {"error": str(e)}
            log_to_file("aider.out.last.log", "/api/chat", error_response, stream=False)
            return JSONResponse(error_response, status_code=500)

    # STREAMING: Forward NDJSON chunks immediately
    async def stream_generator():
        try:
            async with httpx.AsyncClient(timeout=600.0) as client:
                async with client.stream("POST", f"{target}/api/chat", json=data) as resp:
                    response_data = []
                    try:
                        async for line in resp.aiter_lines():
                            if line.strip():
                                yield line
                                try:
                                    chunk_data = json.loads(line)
                                    response_data.append(chunk_data)
                                    log_to_file("aider.out.last.log", "/api/chat", chunk_data, stream=True)
                                except Exception as e:
                                    error_response = {"error": str(e)}
                                    yield json.dumps(error_response)
                    finally:
                        # Append trailing newline to aider.out.last.log without re-logging last chunk
                        log_to_file("aider.out.last.log", "/api/chat", is_final=True)
        except StopAsyncIteration:
            # Handle StopAsyncIteration exception
            pass
        except Exception as e:
            yield json.dumps({"error": str(e)})
            log_to_file("aider.out.last.log", "/api/chat", {"error": str(e)}, stream=stream)

    return StreamingResponse(stream_generator(), media_type="application/x-ndjson")
