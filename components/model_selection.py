import re

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
