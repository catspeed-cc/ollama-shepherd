import os
import sys
from dotenv import load_dotenv
from fastapi import FastAPI, Request
from components.routing_chat import proxy_chat
from components.routing_show import proxy_show

# Load environment variables early so components can access them
load_dotenv()

<<<<<<< HEAD
# Load needed environment variables for use (provide safe defaults)
LOGS_DIR = os.environ.get("LOGS_DIR", "logs")
LOG_FILE = os.environ.get("LOG_FILE", "router.log")
RUN_DIR = os.environ.get("RUN_DIR", "run")
PID_FILE = os.environ.get("PID_FILE", "router.pid")
=======
from components.misc import join_path
>>>>>>> c59cae1 (refactor: improve logging and environment variable handling)

# Validate required environment variables
required_vars = {
    "ARCHITECT_MODEL": os.environ.get("ARCHITECT_MODEL", ""),
    "ARCHITECT_ENDPOINT": os.environ.get("ARCHITECT_ENDPOINT", ""),
    "CODER_MODEL": os.environ.get("CODER_MODEL", ""),
    "CODER_ENDPOINT": os.environ.get("CODER_ENDPOINT", ""),
}

<<<<<<< HEAD
# Immediately exit if any variables are blank - assume something is critically wrong
=======
LOG_ENABLED = os.environ.get("LOG_ENABLED", "False").lower() == "true"

>>>>>>> c59cae1 (refactor: improve logging and environment variable handling)
for var_name, var_value in required_vars.items():
    if not var_value or not var_value.strip():
        error_message = f"""
****************************************************
*  CRITICAL ERROR: Invalid backend configuration!  *
****************************************************
The '{var_name}' variable is empty or contains only whitespace.
Please correct the backend configuration in .env and restart the router.
****************************************************
"""
        
        # Delete PID file if it exists
<<<<<<< HEAD
        pid_file_path = os.path.join(RUN_DIR, PID_FILE)
=======
        RUN_DIR = os.environ.get("RUN_DIR", "run")
        PID_FILE = os.environ.get("PID_FILE", "router.pid")
        pid_file_path = join_path(RUN_DIR, PID_FILE)
>>>>>>> c59cae1 (refactor: improve logging and environment variable handling)
        if os.path.exists(pid_file_path):
            os.remove(pid_file_path)

        # Log error message to file and console
<<<<<<< HEAD
        log_file_path = os.path.join(LOGS_DIR, LOG_FILE)
        with open(log_file_path, "a") as f:
            f.write(error_message)
=======
        if LOG_ENABLED:
            LOGS_DIR = os.environ.get("LOGS_DIR", "logs")
            LOG_FILE = os.environ.get("LOG_FILE", "router.log")
            log_file_path = join_path(LOGS_DIR, LOG_FILE)
            with open(log_file_path, "a") as f:
                f.write(error_message)
>>>>>>> c59cae1 (refactor: improve logging and environment variable handling)
        print(error_message)

        # Terminate execution
        sys.exit(1)

app = FastAPI()

@app.post("/api/chat")
@app.get("/api/chat")
async def chat(request: Request):
    return await proxy_chat(request)

@app.post("/api/show")
@app.get("/api/show")
async def show(request: Request):
    return await proxy_show(request)

if __name__ == "__main__":
    import uvicorn
    
    ROUTER_HOST = os.environ.get("ROUTER_HOST", "0.0.0.0")
    ROUTER_PORT = int(os.environ.get("ROUTER_PORT", 10420))
    LOGS_DIR = os.environ.get("LOGS_DIR", "logs")

    # Create logs directory if missing
    if not os.path.exists(LOGS_DIR):
        os.makedirs(LOGS_DIR)

    uvicorn.run(app, host=ROUTER_HOST, port=ROUTER_PORT)
