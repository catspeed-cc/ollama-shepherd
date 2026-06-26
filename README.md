# Router Description
This router is designed to forward requests to different models based on the requested model.

## Features
* Supports multiple models: qwen3.6:27b, llama3.3:70b, gemma2:9b
* Logs inbound and outbound payloads to files
* Handles streaming and non-streaming requests

## Usage
To start the router, run `./start_router.sh`. The router will listen on a configurable host and port.
The following environment variables can be set to override the default values:
* `ROUTER_HOST`: Host IP address (default: "0.0.0.0")
* `ROUTER_PORT`: Port number (default: 10422)
The following routes are available:
* `/api/chat`: Forwards chat requests to the specified model
* `/api/show`: Forwards show requests to the specified model
Inbound and outbound payloads are logged to `logs/aider.in.last.log` and `logs/aider.out.last.log`, respectively.
