from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, JSONResponse
import httpx, re, json

app = FastAPI()
client = httpx.AsyncClient(timeout=600.0)

MODEL_MAP = {
    "qwen3.6:27b": "http://localhost:11434",    # GPU 1 (Coder)
    "llama3.3:70b": "http://localhost:11435",   # GPU 3 (Reasoner)
    "gemma2:9b": "http://localhost:11436"       # GPU 0 (Fast)
}

def get_target_port(model_name):
    clean = re.sub(r'^ollama_chat/', '', model_name).strip()
    if clean in MODEL_MAP:
        return MODEL_MAP[clean]
    for name, port in MODEL_MAP.items():
        if clean.startswith(name.split(':')[0]):
            return port
    return None

@app.post("/api/chat")
async def proxy_chat(request: Request):
    data = await request.json()
    model = data.get("model", "")
    stream = data.get("stream", False)  # Respect original stream flag

    target = get_target_port(model)
    if not target:
        return JSONResponse({"error": f"Unknown model: {model}"}, status_code=400)

    print(f"DEBUG: Routing '{model}' to {target} (stream={stream})")

    # NON-STREAMING: Wait for full response, return single JSON
    if not stream:
        try:
            resp = await client.post(f"{target}/api/chat", json=data)
            resp.raise_for_status()
            return JSONResponse(content=resp.json())
        except Exception as e:
            return JSONResponse({"error": str(e)}, status_code=500)

    # STREAMING: Forward NDJSON chunks immediately
    async def stream_generator():
        try:
            async with client.stream("POST", f"{target}/api/chat", json=data) as resp:
                async for line in resp.aiter_lines():
                    if line.strip():
                        yield line + "\n"
        except Exception as e:
            yield json.dumps({"error": str(e)}) + "\n"

    return StreamingResponse(stream_generator(), media_type="application/x-ndjson")

@app.post("/api/show")
@app.get("/api/show")
async def proxy_show(request: Request):
    data = await request.json() if request.method == "POST" else {}
    model = data.get("model", "")
    clean = re.sub(r'^ollama_chat/', '', model).strip()
    target = get_target_port(model)

    if target:
        try:
            resp = await client.post(f"{target}/api/show", json={"model": clean})
            return resp.json()
        except:
            pass

    return {
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

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=10422)
