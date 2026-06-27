# Description
This router is designed to forward requests to different models based on the requested model. The routing logic is based on a predefined mapping of model names to their corresponding ports. The `router.py` file contains a dictionary called `MODEL_MAP` that maps model names to their respective ports. When a request is received, the router checks if the requested model is in the `MODEL_MAP`. If it is, the request is forwarded to the corresponding port. If not, the router returns an error response.

# Features
The following features are supported by this router:
* Streaming support: The router can handle streaming requests and responses.
* Logging: The router logs inbound and outbound payloads to files for debugging purposes.
* Model mapping: The router uses a predefined mapping of model names to their corresponding ports to forward requests.

## Model Selection
The `components/model_selection.py` file contains a dictionary called `MODEL_MAP` that maps model names to their respective ports. When a request is received, the router checks if the requested model is in the `MODEL_MAP`. If it is, the request is forwarded to the corresponding port. If not, the router returns an error response.

# Configuration
To configure the router, you need to copy the `.env.example` file to a new file called `.env`. The `.env` file contains environment variables that are used by the router. The following variables are available:
* `ROUTER_HOST`: The host IP address to bind to (default: "0.0.0.0")
* `ROUTER_PORT`: The port number to listen on (default: 10420)
* `LOGS_DIR`: The directory for log files (default: "logs")
* `RUN_DIR`: The directory for the PID file (default: "run")
* `PID_FILE`: The name of the PID file (default: "router.pid")
* `VENV_ACTIVATE`: The path to the virtual environment activation script (default: "/home/aider/aider-venv/bin/activate")

You can modify these variables in the `.env` file to suit your needs.

# Usage
To use the router, follow these steps:
1. Copy the `.env.example` file to a new file called `.env`: `cp .env.example .env`
2. Modify the variables in the `.env` file as needed.
3. Start the router: `./start_router.sh`
4. Verify that the router is running: `ps -ef | grep python`
5. Stop the router: `./stop_router.sh`
6. Verify that the router has stopped: `ps -ef | grep python`

Note: Make sure to replace `/home/aider/aider-venv/bin/activate` with the actual path to your virtual environment activation script.

By following these steps, you can configure and use the router to forward requests to different models based on the requested model.
