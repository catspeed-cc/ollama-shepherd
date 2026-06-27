# Description
This router is designed to sit between Aider (in Architect mode) and one or two Ollama instances, and forward requests to different models based on the requested model.

The routing logic is based on a predefined mapping of model names to their corresponding ports within the `.env` file. When a request is received, the router checks if the requested model is either Architect or Coder and the request is forwarded to the corresponding backend. If unable to route the request, the router returns an error response.

# Features
The following features are supported by this router:
* Streaming support: The router can handle streaming requests and responses.
* Logging: The router logs inbound and outbound payloads to files for debugging purposes.

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

`# Backend Ollama Configuration (REQUIRED):`
* `ARCHITECT_ENDPOINT`: The endpoint URL for the architect model.
* `ARCHITECT_MODEL`: The name of the architect model.
* `CODER_ENDPOINT`: The endpoint URL for the coder model.
* `CODER_MODEL`: The name of the coder model.


You can modify these variables in the `.env` file to suit your needs.

# Backend Ollama Configuration (REQUIRED)
You will be required to configure both the architect and the coder endpoints, and models. The model is auto selected based on which model is requested, and then routed to the model matching either archtect or coder.

There are multiple possible setups:


## Two models share 1 GPU (1 GPU setup)
You will require one backend Ollama with the endpoint exposed on localhost. The downside to this configuration is that the same GPU has to swap models in between Architect and Coder, and each model must fit on the same GPU. Requests fulfilled on same GPU with different models.

An example of this setup, in `.env`:
```
ARCHITECT_ENDPOINT="127.0.0.1:11434"
ARCHITECT_MODEL="llama3.3:70b"
CODER_ENDPOINT="127.0.0.1:11434"
CODER_MODEL="qwen3.6:27b"
```


## Two models exclusively on separate GPU's (2 GPU setup)
This is a more ideal situation, where both GPU's are assigned a model, and they sit idle waiting for requests. When aider sends architect requests, aarouter recognizes the model name, compares to it's configuration, and directs the request to Architect or Coder, the work is sent back to aider.

Critical Considerations:
- If both GPU's are the exact same, don't worry about ensuring Architect/Coder run on correct GPU index as the initial request will download/update the model and select it.
- If both GPU's are different you need to note down which one is the beefier GPU, it's index from `nvidia-smi`, what the largest model it can fit is and which port you assigned it - this will be your "Architect". For the smaller GPU you need to note down it's index from `nvidia-smi`, the largest model it can fit, and what port you assigned it - this will be your "Coder".

An example of this setup, in `.env`:
```
ARCHITECT_ENDPOINT="127.0.0.1:11434"
ARCHITECT_MODEL="llama3.3:70b"
CODER_ENDPOINT="127.0.0.1:11435"
CODER_MODEL="qwen3.6:27b"
```


# Funny story about this project and how it started
I was trying to make an orchestrator model with Leo, and was not doing well. Aider was returned empty responses and we couldn't figure them out. So I decided to take the simple router I made that was working, and just add some logging capability to it, so I can run it in the middle and capture everything to log file, so I could then go and use that data to make my Ollama Orchestrator project.

This is where I noticed that this project is useful as a simple model based router for Aider in Architect mode. Hence the name `aarouter (Aider Architect Router)`

This basic router is already functional and can improve your Aider experience today :)


# You mentioned `Ollama Orchestrator`? Explain.
The AI Ollama Orchestrator is a similar project, but it would sit in between Aider and either two or three models on two or three GPU's. We will implement our own version of `Architect` mode, but we name it a `Supervisor` and it will be automatically handled in the background.

- Commit message generation requests would be immediately passed to the weakest model/GPU (in my case, gemma2:9b on my RTX3070) to generate. 
- Any chat requests would a) replace the system and user prompt, b) send it to a model to *only* reword the prompt with a non-conflicting one and inject our desireable changes to it, c) then place the modified system or user prompts back into the request replacing the original ones. then d) send the modified request back to the Supervisor. This will clear up the confusion between the models and their goals as defined by the user and instead of being confused they will operate more efficiently.

Then we begin the processing loop:
- Supervisor under modified request would analyse the user request sent by Aider, develop a plan to implement it, make its code suggestions as the expert Reasoner
- Coder would then receive the instructions from the supervisor and go to work, hopefully with little or no confusion
- Coder sends work back
- Supervisor intercepts work, audits work, and either a) sends work back to coder for correction or b) returns the response back to Aider
- The above loop feeds itself, and may take a while - eventually we will add config variable thresholds and loop counters

For now the AI Ollama Orchestrator is waiting for this project to succeed :) I will drop links when the repos go live!

~mooleshacat :3
