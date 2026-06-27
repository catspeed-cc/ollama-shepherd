from fastapi import Request
from fastapi.responses import JSONResponse
import httpx
import re
from .logging_utils import log_to_file
from .model_selection import get_target_port

async def proxy_show(request: Request):
    if request.method == "POST":
        data = await request.json()
    else:
        data = {}
    stream = data.get("stream", False)  # Respect original stream flag
    log_to_file("aider.in.last.log", "/api/show", data, stream=stream)

    model = data.get("model", "")
    clean = re.sub(r'^ollama_chat/', '', model).strip()
    target = get_target_port(model)

    if target:
        try:
            async with httpx.AsyncClient(timeout=600.0) as client:
                resp = await client.post(f"{target}/api/show", json={"model": clean})
                response_data = resp.json()
                log_to_file("aider.out.last.log", "/api/show", response_data, stream=stream)
                return response_data
        except Exception as e:
            error_response = {"error": str(e)}
            log_to_file("aider.out.last.log", "/api/show", error_response, stream=stream)
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
    log_to_file("aider.out.last.log", "/api/show", response_data, stream=stream)
    return response_data
