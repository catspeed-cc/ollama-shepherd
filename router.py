from fastapi import FastAPI, Request
import os
from dotenv import load_dotenv

# Load environment variables early so components can access them
load_dotenv()

from components.routing_chat import proxy_chat
from components.routing_show import proxy_show

app = FastAPI()

@app.post("/api/chat")
async def chat(request: Request):
    return await proxy_chat(request)

@app.post("/api/show")
@app.get("/api/show")
async def show(request: Request):
    return await proxy_show(request)

if __name__ == "__main__":
    import uvicorn
    
    HOST = os.environ.get("ROUTER_HOST", "0.0.0.0")
    PORT = int(os.environ.get("ROUTER_PORT", 10420))
    LOGS_DIR = os.environ.get("LOGS_DIR", "logs")

    # Create logs directory if missing
    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR)

    uvicorn.run(app, host=HOST, port=PORT)
