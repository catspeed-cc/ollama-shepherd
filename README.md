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

`# Router Configuration:`
* `ROUTER_HOST`: The host IP address to bind to (default: "0.0.0.0")
* `ROUTER_PORT`: The port number to listen on (default: 10420)
* `ROUTER_TIMEOUT`: The timeout in seconds for HTTP requests made by the router (default: 900.0)

`# Path Configuration:`
* `LOGS_DIR`: The directory for log files (default: "logs")
* `RUN_DIR`: The directory for the PID file (default: "run")
* `VENV_DIR`: The directory for the venv (default: "venv")

`# Filenames:`
* `LOG_FILE`: The main router log filename (default: "router.log")
* `PID_FILE`: The main router PID filename (default: "router.pid")

You can modify these variables in the `.env` file to suit your needs.

# Backend Ollama Configuration
The following environment variables are used to configure the backend ollama endpoints:

* `ARCHITECT_ENDPOINT`: The endpoint URL for the architect model.
* `ARCHITECT_MODEL`: The name of the architect model.
* `CODER_ENDPOINT`: The endpoint URL for the coder model.
* `CODER_MODEL`: The name of the coder model.

These variables should be defined in the `.env` file. For example:
