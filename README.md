# Router Description
This router is designed to forward requests to different models based on the requested model.

## Features
* Supports multiple models: qwen3.6:27b, llama3.3:70b, gemma2:9b
* Logs inbound and outbound payloads to files
* Handles streaming and non-streaming requests

## Usage
To start the router, run `./start_router.sh`. The router will listen on a configurable host and port.

### Environment Variables
The following environment variables can be set in a `.env` file:
