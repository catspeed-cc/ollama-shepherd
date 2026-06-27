import re

# MODEL MAP to route based on MODEL REQUESTED by aider - not GPU index.
MODEL_MAP = {
    # visual separation for human user
    "llama3.3:70b": "http://localhost:11435",   # Architect/Reasoner Endpoint - GPU 1: INDEX: 3
    "llama3.3:70b-desc": "ollama-a100-2",       # Description of Architect/Reasoner Endpoint for human
    # visual separation for human user
    "qwen3.6:27b": "http://localhost:11434",    # Editor/Coder Endpoint - GPU 2: INDEX: 1
    "qwen3.6:27b-desc": "ollama-a100-1"         # Description of Editor/Coder endpoint for human
    # visual separation for human user
}

def get_target_port(model_name):
    clean = re.sub(r'^ollama_chat/', '', model_name).strip()
    if clean in MODEL_MAP:
        return MODEL_MAP[clean]
    for name, port in MODEL_MAP.items():
        if clean.startswith(name.split(':')[0]):
            return port
    return None
