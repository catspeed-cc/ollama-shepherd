from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse, JSONResponse
import httpx, re, json, os
from dotenv import load_dotenv

load_dotenv()

# Variables from environment (provide safe defaults)
HOST = os.environ.get("ROUTER_HOST", "0.0.0.0")
PORT = int(os.environ.get("ROUTER_PORT", 10420))
LOGS_DIR = os.environ.get("LOGS_DIR", "logs")

# Variables not from environment (local variables)
IN_LOG_FILE = "aider.in.last.log"
OUT_LOG_FILE = "aider.out.last.log"

# Create logs directory if missing
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

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

def log_to_file(filename, endpoint, content):
    filepath = os.path.join(LOGS_DIR, filename)
    with open(filepath, 'a') as f:
        json.dump(content, f)
        f.write('\n\n')

@app.post("/api/chat")
async def proxy_chat(request: Request):
    data = await request.json()
    log_to_file(IN_LOG_FILE, "/api/chat", data)

    model = data.get("model", "")
    stream = data.get("stream", False)  # Respect original stream flag

    target = get_target_port(model)
    if not target:
        error_response = {"error": f"Unknown model: {model}"}
        log_to_file(OUT_LOG_FILE, "/api/chat", error_response)
        return JSONResponse(error_response, status_code=400)

    print(f"DEBUG: Routing '{model}' to {target} (stream={stream})")

    # NON-STREAMING: Wait for full response, return single JSON
    if not stream:
        try:
            resp = await client.post(f"{target}/api/chat", json=data)
            resp.raise_for_status()
            response_data = resp.json()
            log_to_file(OUT_LOG_FILE, "/api/chat", response_data)
            return JSONResponse(content=response_data)
        except Exception as e:
            error_response = {"error": str(e)}
            log_to_file(OUT_LOG_FILE, "/api/chat", error_response)
            return JSONResponse(error_response, status_code=500)

    # STREAMING: Forward NDJSON chunks immediately
    async def stream_generator():
        try:
            async with client.stream("POST", f"{target}/api/chat", json=data) as resp:
                response_data = []
                async for line in resp.aiter_lines():
                    if line.strip():
                        yield line + "\n"
                        try:
                            chunk_data = json.loads(line)
                            response_data.append(chunk_data)
                        except Exception as e:
                            error_response = {"error": str(e)}
                            yield json.dumps(error_response) + "\n"
                log_to_file(OUT_LOG_FILE, "/api/chat", response_data)
        except Exception as e:
            yield json.dumps({"error": str(e)}) + "\n"
            log_to_file(OUT_LOG_FILE, "/api/chat", {"error": str(e)})

    return StreamingResponse(stream_generator(), media_type="application/x-ndjson")

@app.post("/api/show")
@app.get("/api/show")
async def proxy_show(request: Request):
    if request.method == "POST":
        data = await request.json()
    else:
        data = {}
    log_to_file(IN_LOG_FILE, "/api/show", data)

    model = data.get("model", "")
    clean = re.sub(r'^ollama_chat/', '', model).strip()
    target = get_target_port(model)

    if target:
        try:
            resp = await client.post(f"{target}/api/show", json={"model": clean})
            response_data = resp.json()
            log_to_file(OUT_LOG_FILE, "/api/show", response_data)
            return response_data
        except Exception as e:
            error_response = {"error": str(e)}
            log_to_file(OUT_LOG_FILE, "/api/show", error_response)
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
    log_to_file(OUT_LOG_FILE, "/api/show", response_data)
    return response_data

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host=HOST, port=PORT)
